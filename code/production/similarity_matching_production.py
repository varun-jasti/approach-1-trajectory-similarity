#!/usr/bin/env python3
"""
Similarity-based agent matching — replaces random emp_only fallback.

Old Step 2 (when exact home_taz match fails):
  Pick a random agent with same employment from anywhere in county.

New Step 2 (this script):
  1. Build 6D feature vectors for all real agents:
       [home_lat_norm, home_lon_norm,
        act1_clat_norm, act1_clon_norm,
        act2_clat_norm, act2_clon_norm]
  2. For each synthetic person (emp_only rows): find same-employment agents
     with home TAZ centroid within NEARBY_KM radius (default 15 km).
  3. Among those candidates, pick the one with minimum Manhattan distance
     on the 6D feature vector (cosine would also work; Manhattan is simpler
     to explain and avoids magnitude bias).
  4. Fallback: expand radius to 30 km, then county-wide if still empty.

After re-matching, activity and activity_taz are updated from the new agent,
and poi fields are cleared to trigger hierarchical TAZ re-assignment.

Output: Approach_3/03_RESULTS/A3_final.parquet
"""

import time, gc
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.spatial import KDTree

t0 = time.time()
def ts(): return f"[{time.time()-t0:>6.1f}s]"

A3_IN    = 'Approach_3/03_RESULTS/A3_fixed_hierarchical.parquet'
A3_TMP   = 'Approach_3/03_RESULTS/A3_similarity_tmp.parquet'
A3_OUT   = 'Approach_3/03_RESULTS/A3_final.parquet'
PROF_PATH= 'Approach_3/01_INPUTS/agent_trajectory_profiles.parquet'
POI_PATH = 'Approach_2/phase 3/poi_with_taz.parquet'
REPORT   = 'Approach_3/05_VALIDATION/similarity_matching_report.txt'

NEARBY_KM   = 15.0   # primary radius for nearby-TAZ search
FALLBACK_KM = 30.0   # expanded radius if primary finds nothing
TOP_K       = 5      # sample from top-K similar agents (adds diversity)

RING1_KM  = 5.0
RING2_KM  = 15.0
K_NEAREST = 50

print("=" * 65)
print("SIMILARITY-BASED AGENT MATCHING")
print(f"  Primary radius   : {NEARBY_KM} km")
print(f"  Fallback radius  : {FALLBACK_KM} km")
print(f"  Feature vector   : 6D [home_lat/lon + act1_lat/lon + act2_lat/lon]")
print(f"  Distance metric  : Manhattan (normalized features)")
print("=" * 65)

# ── TAZ centroid map ──────────────────────────────────────────────────────────
print(f"\n{ts()} Building TAZ centroid map from POI data...")
poi_df = pq.read_table(POI_PATH, columns=['taz_id','latitude','longitude']).to_pandas()
poi_df['taz_str'] = poi_df['taz_id'].apply(lambda x: str(int(float(x))) if pd.notna(x) else None)
poi_df = poi_df.dropna(subset=['taz_str'])
taz_cent = poi_df.groupby('taz_str').agg(clat=('latitude','mean'), clon=('longitude','mean')).reset_index()
taz_clat = taz_cent.set_index('taz_str')['clat'].to_dict()
taz_clon = taz_cent.set_index('taz_str')['clon'].to_dict()
del poi_df; gc.collect()

def norm_taz(x):
    try: return str(int(float(x)))
    except: return None

def taz_to_latlon(taz_str):
    t = norm_taz(taz_str)
    if t and t in taz_clat:
        return taz_clat[t], taz_clon[t]
    return np.nan, np.nan

print(f"  {len(taz_clat):,} TAZ centroids loaded")

# ── Load agent profiles ───────────────────────────────────────────────────────
print(f"\n{ts()} Loading agent profiles and building similarity index...")
prof = pq.read_table(PROF_PATH).to_pandas()

# Get lat/lon centroids for home, act1, act2 TAZs
prof['home_str']  = prof['home_taz'].apply(norm_taz)
prof['act1_str']  = prof['act1_taz'].apply(norm_taz)
prof['act2_str']  = prof['act2_taz'].apply(norm_taz)

prof['home_clat'] = prof['home_str'].map(taz_clat)
prof['home_clon'] = prof['home_str'].map(taz_clon)
prof['act1_clat'] = prof['act1_str'].map(taz_clat)
prof['act1_clon'] = prof['act1_str'].map(taz_clon)
prof['act2_clat'] = prof['act2_str'].map(taz_clat)
prof['act2_clon'] = prof['act2_str'].map(taz_clon)

# Drop agents with missing home centroid (can't use for geographic matching)
prof = prof.dropna(subset=['home_clat', 'home_clon']).reset_index(drop=True)

# Fill missing act TAZ centroids with home centroid (conservative fallback)
for col in ['act1_clat','act2_clat']:
    prof[col] = prof[col].fillna(prof['home_clat'])
for col in ['act1_clon','act2_clon']:
    prof[col] = prof[col].fillna(prof['home_clon'])

print(f"  {len(prof):,} agents with valid home centroids")

# Normalize each coordinate column to [0, 1] across all agents
feat_cols = ['home_clat','home_clon','act1_clat','act1_clon','act2_clat','act2_clon']
feat_min = prof[feat_cols].min()
feat_max = prof[feat_cols].max()
feat_range = (feat_max - feat_min).replace(0, 1)

prof_norm = (prof[feat_cols] - feat_min) / feat_range   # (n_agents, 6)
feat_matrix = prof_norm.values.astype(np.float32)        # (n_agents, 6)

# Per-employment KDTree on home lat/lon (for fast radius search)
emp_trees  = {}  # employment → KDTree on (home_clat, home_clon) in radians
emp_arrays = {}  # employment → row indices into prof

for emp, grp in prof.groupby('employment'):
    coords = np.radians(grp[['home_clat','home_clon']].values)
    emp_trees[emp]  = KDTree(coords)
    emp_arrays[emp] = grp.index.values   # index into prof / feat_matrix

print(f"  KDTrees built for: {list(emp_trees.keys())}")

# ── Build lookup: (employment, home_taz_str) → best matched agent ─────────────
print(f"\n{ts()} Building similarity match lookup for all emp_only combos...")

# Read all emp_only rows to find unique (employment, home_taz) combos
pf_in = pq.ParquetFile(A3_IN)
emp_only_combos = set()
for rg in range(pf_in.num_row_groups):
    c = pf_in.read_row_group(rg, columns=['employment','home_taz','match_type','step']).to_pandas()
    fb = c[(c['match_type'] == 'emp_only') & (c['step'] == 1)]
    for _, row in fb[['employment','home_taz']].drop_duplicates().iterrows():
        emp_only_combos.add((str(row['employment']), norm_taz(row['home_taz'])))

print(f"  {len(emp_only_combos):,} unique (employment, home_taz) combos to re-match")

# For each combo, find the best nearby similar agent
combo_match = {}   # (employment, home_taz_str) → {caid, act1, act2, act1_taz, act2_taz, match_type}
stats = {'primary': 0, 'fallback': 0, 'county': 0, 'none': 0}

# Pre-build normalized feature vectors for lookup
person_feat_template = np.zeros(6, dtype=np.float32)

for emp, htaz_str in sorted(emp_only_combos, key=lambda x: (x[0] or '', x[1] or '')):
    p_lat, p_lon = taz_to_latlon(htaz_str)
    if np.isnan(p_lat):
        stats['none'] += 1
        combo_match[(emp, htaz_str)] = None
        continue

    # Normalized person feature: use home centroid for all 6 dims
    # (activity positions unknown; home used as neutral prior)
    p_raw = np.array([p_lat, p_lon, p_lat, p_lon, p_lat, p_lon], dtype=np.float32)
    p_norm = (p_raw - feat_min[feat_cols].values) / feat_range[feat_cols].values

    if emp not in emp_trees:
        stats['none'] += 1
        combo_match[(emp, htaz_str)] = None
        continue

    tree    = emp_trees[emp]
    indices = emp_arrays[emp]   # row indices into prof

    # Try primary radius
    q_rad  = np.radians([p_lat, p_lon])
    # KDTree uses radians; convert km to radians (earth radius ~6371 km)
    def km_to_rad(km): return km / 6371.0

    candidate_idxs_tree = tree.query_ball_point(q_rad, r=km_to_rad(NEARBY_KM))
    mtype = 'similarity_nearby'

    if len(candidate_idxs_tree) == 0:
        candidate_idxs_tree = tree.query_ball_point(q_rad, r=km_to_rad(FALLBACK_KM))
        mtype = 'similarity_fallback'

    if len(candidate_idxs_tree) == 0:
        # County-wide — use all same-employment agents
        candidate_idxs_tree = list(range(len(indices)))
        mtype = 'emp_only_county'

    # Map tree indices back to prof indices
    cand_prof_idxs = indices[candidate_idxs_tree]

    # Compute Manhattan distance on 6D normalized feature vector
    cand_feats = feat_matrix[cand_prof_idxs]          # (n_cands, 6)
    dists      = np.abs(cand_feats - p_norm).sum(axis=1)  # Manhattan

    # Sample from top-K to add diversity (avoid always picking one popular agent)
    k        = min(TOP_K, len(dists))
    top_k    = np.argpartition(dists, k - 1)[:k]
    best_loc = top_k[np.random.randint(k)]   # random from top-K
    best_idx = cand_prof_idxs[best_loc]

    agent = prof.iloc[best_idx]
    combo_match[(emp, htaz_str)] = {
        'caid':     agent['caid'],
        'act1':     agent['act1'],
        'act2':     agent['act2'],
        'act1_taz': norm_taz(agent['act1_taz']),
        'act2_taz': norm_taz(agent['act2_taz']),
        'mtype':    mtype,
    }

    if   mtype == 'similarity_nearby':   stats['primary']  += 1
    elif mtype == 'similarity_fallback': stats['fallback'] += 1
    else:                                stats['county']   += 1

print(f"  Results: primary={stats['primary']:,}  fallback={stats['fallback']:,}  "
      f"county={stats['county']:,}  none={stats['none']:,}")

# ── Apply re-matching to A3 data ──────────────────────────────────────────────
print(f"\n{ts()} Applying similarity matches and clearing POI for re-assignment...")

# Also load POI data + hierarchical tools for POI re-assignment
poi_df_full = pq.read_table(POI_PATH).to_pandas()
poi_df_full = poi_df_full.dropna(subset=['latitude','longitude','taz_id','activity_label1'])
poi_df_full['taz_str'] = poi_df_full['taz_id'].apply(
    lambda x: str(int(float(x))) if pd.notna(x) else None)
poi_df_full = poi_df_full.dropna(subset=['taz_str'])

act_trees_h = {}
act_pois_h  = {}
for act, grp in poi_df_full.groupby('activity_label1'):
    grp = grp.reset_index(drop=True)
    act_trees_h[act] = KDTree(np.radians(grp[['latitude','longitude']].values))
    act_pois_h[act]  = grp

def haversine_1d(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1))*np.cos(np.radians(lat2))*np.sin(dlon/2)**2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

def haversine_2d(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = (np.sin(dlat/2)**2 +
         np.cos(np.radians(lat1))*np.cos(np.radians(lat2))*np.sin(dlon/2)**2)
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

def assign_poi_hierarchical(activity, activity_taz_str, home_lat, home_lon, K=K_NEAREST):
    """Find best POI using ring hierarchy. Returns (poi_row, ring_int) or (None, -1)."""
    if activity not in act_trees_h:
        return None, -1
    tree = act_trees_h[activity]
    pois = act_pois_h[activity]
    K_   = min(K, len(pois))

    q_lat = taz_clat.get(activity_taz_str, home_lat)
    q_lon = taz_clon.get(activity_taz_str, home_lon)
    _, idxs = tree.query(np.radians([[q_lat, q_lon]]), k=K_)
    cands = pois.iloc[idxs[0]].reset_index(drop=True)

    act_clat_ = taz_clat.get(activity_taz_str, np.nan)
    act_clon_ = taz_clon.get(activity_taz_str, np.nan)

    if np.isnan(act_clat_):
        dh = haversine_1d(home_lat, home_lon, cands['latitude'].values, cands['longitude'].values)
        return cands.iloc[np.argmin(dh)], 3

    c_taz  = cands['taz_str'].values
    c_clat = np.array([taz_clat.get(t, act_clat_) for t in c_taz])
    c_clon = np.array([taz_clon.get(t, act_clon_) for t in c_taz])
    tdist  = haversine_1d(act_clat_, act_clon_, c_clat, c_clon)
    hdist  = haversine_1d(home_lat, home_lon, cands['latitude'].values, cands['longitude'].values)

    ring0 = cands[c_taz == activity_taz_str]
    if len(ring0):
        dh = haversine_1d(home_lat, home_lon, ring0['latitude'].values, ring0['longitude'].values)
        return ring0.iloc[np.argmin(dh)], 0
    r1 = cands[tdist <= RING1_KM]
    if len(r1):
        dh = haversine_1d(home_lat, home_lon, r1['latitude'].values, r1['longitude'].values)
        return r1.iloc[np.argmin(dh)], 1
    r2 = cands[tdist <= RING2_KM]
    if len(r2):
        dh = haversine_1d(home_lat, home_lon, r2['latitude'].values, r2['longitude'].values)
        return r2.iloc[np.argmin(dh)], 2
    return cands.iloc[np.argmin(hdist)], 3

writer = None
update_stats = {'rematched': 0, 'act_changed': 0, 'poi_updated': 0,
                'ring0': 0, 'ring1': 0, 'ring2': 0, 'ring3': 0}

for rg in range(pf_in.num_row_groups):
    rg_t = time.time()
    chunk = pf_in.read_row_group(rg).to_pandas()

    emp_mask = chunk['match_type'] == 'emp_only'

    for pos in np.where(emp_mask)[0]:
        row = chunk.iloc[pos]
        emp = str(row['employment'])
        htaz = norm_taz(row['home_taz'])
        key = (emp, htaz)
        match = combo_match.get(key)
        if match is None:
            continue

        update_stats['rematched'] += 1
        chunk.at[chunk.index[pos], 'matched_caid'] = match['caid']
        chunk.at[chunk.index[pos], 'match_type']   = match['mtype']

        step = int(row['step'])
        if step == 1:
            new_act = match['act1']
            new_taz = match['act1_taz'] or htaz
        elif step == 2:
            new_act = match['act2']
            new_taz = match['act2_taz'] or htaz
        else:
            continue

        old_act = row['activity']
        if old_act != new_act:
            update_stats['act_changed'] += 1
            chunk.at[chunk.index[pos], 'activity'] = new_act

        if new_taz != norm_taz(row['activity_taz']):
            chunk.at[chunk.index[pos], 'activity_taz'] = new_taz

        # Re-assign POI using hierarchical search in new activity_taz
        home_lat = row.get('home_lat', np.nan)
        home_lon = row.get('home_lon', np.nan)
        if pd.isna(home_lat) or pd.isna(home_lon):
            continue

        poi_row, ring = assign_poi_hierarchical(new_act, new_taz, home_lat, home_lon)
        if poi_row is not None:
            chunk.at[chunk.index[pos], 'poi_name']           = poi_row.get('location_name', '')
            chunk.at[chunk.index[pos], 'poi_category']        = poi_row.get('top_category', '')
            chunk.at[chunk.index[pos], 'poi_lat']             = poi_row['latitude']
            chunk.at[chunk.index[pos], 'poi_lon']             = poi_row['longitude']
            chunk.at[chunk.index[pos], 'safegraph_place_id']  = poi_row.get('safegraph_place_id', '')
            chunk.at[chunk.index[pos], 'poi_taz']             = poi_row['taz_str']
            chunk.at[chunk.index[pos], 'distance_km']         = float(
                haversine_1d(home_lat, home_lon, poi_row['latitude'], poi_row['longitude']))
            update_stats['poi_updated'] += 1
            update_stats[f'ring{ring}'] += 1

    tbl = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter(A3_TMP, tbl.schema, compression='snappy')
    writer.write_table(tbl)
    del chunk, tbl; gc.collect()
    print(f"  RG {rg}: re-matched={update_stats['rematched']:,}  "
          f"act_changed={update_stats['act_changed']:,}  "
          f"poi_updated={update_stats['poi_updated']:,}  "
          f"{time.time()-rg_t:.1f}s")

if writer:
    writer.close()

import os
os.replace(A3_TMP, A3_OUT)
print(f"\n{ts()} Written → {A3_OUT}")

# ── Validation ────────────────────────────────────────────────────────────────
print(f"\n{ts()} Computing final match_type distribution...")
sample = pq.read_table(A3_OUT, columns=['match_type','distance_km','activity']).to_pandas()
mc = sample['match_type'].value_counts()
total = len(sample)
print("\nFinal match_type distribution:")
for mt, cnt in mc.items():
    print(f"  {mt:<30} {cnt:>10,}  ({cnt/total*100:.1f}%)")

non_home = sample[~sample['activity'].str.lower().str.contains('home', na=False)]
non_home = non_home[non_home['distance_km'].notna() & (non_home['distance_km'] > 0) & (non_home['distance_km'] < 100)]
print(f"\nDistance stats (non-home trips, n={len(non_home):,}):")
print(f"  Median : {non_home['distance_km'].median():.2f} km")
print(f"  Mean   : {non_home['distance_km'].mean():.2f} km")
print(f"  P95    : {non_home['distance_km'].quantile(0.95):.2f} km")

# ── Report ────────────────────────────────────────────────────────────────────
report = f"""SIMILARITY-BASED AGENT MATCHING — REPORT
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

METHODOLOGY:
  Feature vector (6D, Manhattan distance):
    [home_lat_norm, home_lon_norm,
     act1_TAZ_centroid_lat_norm, act1_TAZ_centroid_lon_norm,
     act2_TAZ_centroid_lat_norm, act2_TAZ_centroid_lon_norm]
  Primary search radius  : {NEARBY_KM} km
  Fallback search radius : {FALLBACK_KM} km
  Top-K sampling         : {TOP_K} (diversity)

COMBO RESOLUTION ({len(emp_only_combos):,} unique employment+home_TAZ combos):
  Resolved in primary radius  ({NEARBY_KM} km) : {stats['primary']:>8,}  ({stats['primary']/len(emp_only_combos)*100:.1f}%)
  Resolved in fallback radius ({FALLBACK_KM} km) : {stats['fallback']:>8,}  ({stats['fallback']/len(emp_only_combos)*100:.1f}%)
  County-wide (no nearby found)               : {stats['county']:>8,}  ({stats['county']/len(emp_only_combos)*100:.1f}%)
  Failed (no TAZ centroid)                    : {stats['none']:>8,}  ({stats['none']/len(emp_only_combos)*100:.1f}%)

ROW UPDATES:
  Rows re-matched          : {update_stats['rematched']:>10,}
  Activity type changed    : {update_stats['act_changed']:>10,}
  POI re-assigned          : {update_stats['poi_updated']:>10,}
    Ring 0 (exact TAZ)     : {update_stats['ring0']:>10,}  ({update_stats['ring0']/max(update_stats['poi_updated'],1)*100:.1f}%)
    Ring 1 (adjacent)      : {update_stats['ring1']:>10,}  ({update_stats['ring1']/max(update_stats['poi_updated'],1)*100:.1f}%)
    Ring 2 (regional)      : {update_stats['ring2']:>10,}  ({update_stats['ring2']/max(update_stats['poi_updated'],1)*100:.1f}%)
    Ring 3 (county)        : {update_stats['ring3']:>10,}  ({update_stats['ring3']/max(update_stats['poi_updated'],1)*100:.1f}%)

FINAL MATCH TYPE DISTRIBUTION:
"""
for mt, cnt in mc.items():
    report += f"  {mt:<30} {cnt:>10,}  ({cnt/total*100:.1f}%)\n"

report += f"""
DISTANCE STATS (non-home, n={len(non_home):,}):
  Median : {non_home['distance_km'].median():.2f} km
  Mean   : {non_home['distance_km'].mean():.2f} km
  P95    : {non_home['distance_km'].quantile(0.95):.2f} km
"""
with open(REPORT, 'w') as f:
    f.write(report)
print(f"\n{ts()} Report saved → {REPORT}")
print(f"{ts()} Done.")
