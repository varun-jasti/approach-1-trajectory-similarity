#!/usr/bin/env python3
"""
APPROACH 1 FIX — Chunked row-group processing (memory-safe)
Processes one 1M-row chunk at a time. Peak RAM ~800 MB.
"""

import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.spatial import KDTree
import gc, time

t0 = time.time()
def ts(): return f"[{time.time()-t0:>6.1f}s]"

A3_PATH  = 'path/to/A3_with_confidence.parquet'
OUT_PATH = 'path/to/A3_fixed.parquet'

print("=" * 70)
print("APPROACH 1 FIX — Row-Group Chunked Processing")
print("=" * 70)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    a = np.sin(np.radians(lat2-lat1)/2)**2 + \
        np.cos(np.radians(lat1))*np.cos(np.radians(lat2))*np.sin(np.radians(lon2-lon1)/2)**2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

DIST_CAP = {
    'Buy goods (groceries, clothes, gas)':                                        20,
    'Buy food (go to the restaurant, food, carry-out)':                           15,
    'Work-related activity, or volunteer':                                         45,
    'Attend school':                                                               25,
    'Recreational activities (visit parks, movies, bars) or holidays like hotel': 40,
    'Exercise (jog/walk, walk the dog, gym, diving, etc)':                        20,
    'Buy services (banking, service or repair a car, dry cleaners)':              20,
    'Health care visit (medical, dental, therapy)':                               40,
    'Religious or community activities':                                           20,
    'Visit friends or relatives':                                                  50,
    'Drop off/pick up someone':                                                    50,
    'Attend child or adult care':                                                  20,
    'General errands (post office, library)':                                      15,
    'Something else':                                                              60,
}
IDEAL_BOUNDS = {
    'Buy goods (groceries, clothes, gas)':                                        (0.5, 12),
    'Buy food (go to the restaurant, food, carry-out)':                           (0.5, 8),
    'Work-related activity, or volunteer':                                         (5, 20),
    'Attend school':                                                               (3, 15),
    'Recreational activities (visit parks, movies, bars) or holidays like hotel': (1, 20),
    'Exercise (jog/walk, walk the dog, gym, diving, etc)':                        (0.5, 15),
    'Buy services (banking, service or repair a car, dry cleaners)':              (0.5, 10),
    'Health care visit (medical, dental, therapy)':                               (2, 30),
}

# ── Load support data once ───────────────────────────────────────────────────
print(f"\n{ts()} Loading support data...")

prof = pd.read_parquet('path/to/agent_trajectory_profiles.parquet')
prof = prof.set_index('caid')
print(f"{ts()} {len(prof):,} agent profiles")

poi = pd.read_csv(
    'path/to/Orlando_Metro_poi_activity_labels.csv',
    usecols=['SAFEGRAPH_PLACE_ID','LOCATION_NAME','LATITUDE','LONGITUDE',
             'TOP_CATEGORY','activity_label1','activity_label2']
).dropna(subset=['LATITUDE','LONGITUDE'])
print(f"{ts()} {len(poi):,} POIs")

shard01 = pd.read_parquet(
    'path/to/shard01_activity_labelled_final.parquet',
    columns=['taz_id_cfrpm7','final_latitude','final_longitude'])
taz_lat = shard01.groupby('taz_id_cfrpm7')['final_latitude'].mean().to_dict()
taz_lon = shard01.groupby('taz_id_cfrpm7')['final_longitude'].mean().to_dict()
del shard01; gc.collect()
print(f"{ts()} {len(taz_lat):,} TAZ centroids")

activity_trees, activity_pois = {}, {}
for act in DIST_CAP:
    mask = (poi['activity_label1'] == act) | (poi['activity_label2'] == act)
    sub  = poi[mask].reset_index(drop=True)
    if len(sub) == 0:
        sub = poi.reset_index(drop=True)
    activity_trees[act] = KDTree(np.radians(sub[['LATITUDE','LONGITUDE']].values))
    activity_pois[act]  = sub
print(f"{ts()} {len(activity_trees)} activity KD-trees built")

# ── Process row groups one at a time ─────────────────────────────────────────
pf = pq.ParquetFile(A3_PATH)
n_rg = pf.metadata.num_row_groups
print(f"\n{ts()} Processing {n_rg} row groups ({pf.metadata.num_rows:,} rows total)")

writer = None
stats = {'total': 0, 'reassigned': 0, 'capped': 0}

def realism(act, dist):
    lo, hi = IDEAL_BOUNDS.get(act, (0, 50))
    if lo <= dist <= hi:             return 1.0
    if lo*0.6 <= dist <= hi*1.25:   return 0.7
    if dist <= hi*1.875:             return 0.5
    return 0.2

for rg_idx in range(n_rg):
    chunk = pf.read_row_group(rg_idx).to_pandas()
    n = len(chunk)
    stats['total'] += n
    print(f"{ts()} RG {rg_idx+1}/{n_rg}: {n:,} rows", end='', flush=True)

    # Merge agent profiles for this chunk only
    agent_info = prof.reindex(chunk['matched_caid'].values)[
        ['home_taz','act1','act2','act1_taz','act2_taz']].reset_index(drop=True)

    chunk['agent_home_taz'] = agent_info['home_taz'].values
    chunk['agent_act_taz']  = np.where(
        chunk['activity'].values == agent_info['act1'].values,
        agent_info['act1_taz'].values,
        np.where(chunk['activity'].values == agent_info['act2'].values,
                 agent_info['act2_taz'].values, None))

    chunk['agent_home_lat'] = pd.Series(chunk['agent_home_taz']).map(taz_lat).values
    chunk['agent_home_lon'] = pd.Series(chunk['agent_home_taz']).map(taz_lon).values
    chunk['agent_act_lat']  = pd.Series(chunk['agent_act_taz']).map(taz_lat).values
    chunk['agent_act_lon']  = pd.Series(chunk['agent_act_taz']).map(taz_lon).values

    chunk['target_lat'] = chunk['home_lat'] + chunk['agent_act_lat'] - chunk['agent_home_lat']
    chunk['target_lon'] = chunk['home_lon'] + chunk['agent_act_lon'] - chunk['agent_home_lon']

    is_home    = chunk['activity'].str.lower().str.contains('home', na=False)
    has_target = chunk['target_lat'].notna() & chunk['target_lon'].notna()
    eligible   = ~is_home & has_target

    if eligible.any():
        chunk.loc[eligible, 'target_dist'] = haversine(
            chunk.loc[eligible,'home_lat'].values,
            chunk.loc[eligible,'home_lon'].values,
            chunk.loc[eligible,'target_lat'].values,
            chunk.loc[eligible,'target_lon'].values)

        for act, cap in DIST_CAP.items():
            act_mask = eligible & (chunk['activity'] == act)
            if not act_mask.any():
                continue
            tree    = activity_trees[act]
            act_poi = activity_pois[act]

            within = act_mask & (chunk.get('target_dist', pd.Series(999, index=chunk.index)) <= cap)
            over   = act_mask & ~within

            for mask_part, coord_cols in [(within, ['target_lat','target_lon']),
                                          (over,   ['home_lat','home_lon'])]:
                if not mask_part.any():
                    continue
                q = np.radians(chunk.loc[mask_part, coord_cols].values)
                _, idxs = tree.query(q, k=1)
                m = act_poi.iloc[idxs].reset_index(drop=True)
                pos = np.where(mask_part)[0]
                chunk.iloc[pos, chunk.columns.get_loc('safegraph_place_id')] = m['SAFEGRAPH_PLACE_ID'].values
                chunk.iloc[pos, chunk.columns.get_loc('poi_name')]           = m['LOCATION_NAME'].values
                chunk.iloc[pos, chunk.columns.get_loc('poi_category')]       = m['TOP_CATEGORY'].values
                chunk.iloc[pos, chunk.columns.get_loc('poi_lat')]            = m['LATITUDE'].values
                chunk.iloc[pos, chunk.columns.get_loc('poi_lon')]            = m['LONGITUDE'].values
                if mask_part is over:
                    stats['capped'] += mask_part.sum()

        # Recalculate distances for reassigned rows
        pos = np.where(eligible)[0]
        chunk.iloc[pos, chunk.columns.get_loc('distance_km')] = haversine(
            chunk.loc[eligible,'home_lat'].values,
            chunk.loc[eligible,'home_lon'].values,
            chunk.iloc[pos, chunk.columns.get_loc('poi_lat')].values,
            chunk.iloc[pos, chunk.columns.get_loc('poi_lon')].values)

        stats['reassigned'] += eligible.sum()

    # Recompute factor_distance_realism
    chunk['factor_distance_realism'] = [
        realism(a, d) for a, d in zip(chunk['activity'], chunk['distance_km'])]

    # Drop temp columns
    chunk.drop(columns=[c for c in ['agent_home_taz','agent_act_taz','agent_home_lat',
        'agent_home_lon','agent_act_lat','agent_act_lon','target_lat','target_lon',
        'target_dist'] if c in chunk.columns], inplace=True)

    # Write
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter(OUT_PATH, table.schema, compression='snappy')
    writer.write_table(table)

    del chunk, agent_info, table; gc.collect()
    print(f"  → reassigned={eligible.sum():,}")

if writer:
    writer.close()

# ── Final report ─────────────────────────────────────────────────────────────
print(f"\n{ts()} Saved → {OUT_PATH}")
print(f"\n{'='*70}")
print(f"SUMMARY")
print(f"{'='*70}")
print(f"  Total rows     : {stats['total']:,}")
print(f"  Reassigned     : {stats['reassigned']:,} ({stats['reassigned']/stats['total']*100:.1f}%)")
print(f"  Capped fallback: {stats['capped']:,}  (target too far → used home)")

print(f"\n{ts()} Loading comparison...")
orig = pd.read_parquet(A3_PATH,     columns=['activity','distance_km','person_id'])
fixed = pd.read_parquet(OUT_PATH,   columns=['activity','distance_km','person_id'])
VERASET = {'median':6.10,'<5':42.8,'5-20':44.1,'>20':13.1,'>30':5.2}

print(f"\n{'='*70}")
print("Buy Goods Distance:  Original A3  →  Fixed A3  (Veraset target)")
print(f"{'='*70}")
for label, df in [('Original', orig), ('Fixed', fixed)]:
    d = df[df['activity'].str.contains('Buy goods', na=False)]['distance_km']
    print(f"  {label}:  median={d.median():.2f}km  <5={( d<5).mean()*100:.1f}%  5-20={((d>=5)&(d<=20)).mean()*100:.1f}%  >30={( d>30).mean()*100:.1f}%")
print(f"  Veraset:  median={VERASET['median']}km  <5={VERASET['<5']}%  5-20={VERASET['5-20']}%  >30={VERASET['>30']}%")

print(f"\nSpot-check 100003_1:")
p = fixed[fixed['person_id']=='100003_1']
print(p[['activity','distance_km']].to_string())
print(f"\n{ts()} DONE.")
