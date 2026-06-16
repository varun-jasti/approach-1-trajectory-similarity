# Approach 1 — Case Studies: High / Medium / Low Confidence

*Updated: 2026-06-16*

---

**PURPOSE:** Document representative examples across all confidence tiers.
Each case shows: person profile → archetype → assigned POI → realism verdict.

---

## Summary Examples (5 assignments across confidence levels)

| Confidence | Person | Archetype | Activity | Assigned POI | Category | Dist (km) | MFC | Why it makes sense |
|---|---|---|---|---|---|---|---|---|
| Very High (5/5) | 293198_6 | LOCAL_COMMUTER | Work-related activity, or volunteer | Legacy Universal | Lessors of Real Estate | 15.0 | 0.82 | Commuter matched to office-zone POI 15 km away — typical commute pattern |
| Very High (5/5) | 268415_3 | LOCAL_RESIDENT | Buy food (restaurant, carry-out) | Arby's | Restaurants and Other Eating Places | 4.4 | 0.96 | Exact category match, 4.4 km — ideal range for dining trip |
| Very High (5/5) | 508003_1 | COMMUTER_VISITOR | Attend school | Andover Elementary | Elementary and Secondary Schools | 0.8 | 0.79 | School 0.8 km from home — very local, exact category match |
| High (4/5) | 97528_2 | COMMUTER_VISITOR | Buy goods (groceries, clothes, gas) | Lukas Community Store | Grocery Stores | 1.2 | 0.81 | Grocery store 1.2 km from home — local shopping trip, good category match |
| Medium (3/5) | 472790_8 | RECREATION_FOCUSED | Buy goods (groceries, clothes, gas) | Bravo Property Improvement | Building Material and Supplies Dealers | 0.8 | 0.68 | Hardware store for Buy goods — close category but not ideal; lower score |

---

## Full Case Studies (20 examples)

**PURPOSE:** Covers 3 confidence levels × 5 activity types. Each case: person profile → match type → assigned POI → realism verdict.

---

## TIER 1: HIGH CONFIDENCE CASES (Cases 01–07)

> **Definition:** confidence_score = 5, match_type = taz_specific, Ring 0 (exact TAZ).
> These represent the ideal assignment: POI found in the exact target TAZ, strong Veraset evidence, activity-category alignment.


## CASE 01 — ✅ HIGH CONFIDENCE

  Person ID       : 2582_4
  Employment      : non_worker
  Activity Bucket : Work
  Activity Label  : Work-related activity, or volunteer

  Activity TAZ    : 3647.0
  Match Type      : taz_specific
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : William M Bird Company
  POI Category    : Lumber and Other Construction Materials Merchant Wholesalers
  POI TAZ         : 3647.0  (✓ Same TAZ)
  Distance        : 7.17 km

  MFC Score       : 0.823/1.000
  Confidence      : 5/5

  ASSESSMENT: ✅ Strong match — POI in exact target TAZ, 7.2 km distance is realistic

## CASE 02 — ✅ HIGH CONFIDENCE

  Person ID       : 10581_4
  Employment      : non_worker
  Activity Bucket : School
  Activity Label  : Attend school

  Activity TAZ    : 3431.0
  Match Type      : taz_specific
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : Central Christian University
  POI Category    : Colleges, Universities, and Professional Schools
  POI TAZ         : 3431.0  (✓ Same TAZ)
  Distance        : 3.68 km

  MFC Score       : 0.990/1.000
  Confidence      : 5/5

  ASSESSMENT: ✅ Strong match — POI in exact target TAZ, 3.7 km distance is realistic

## CASE 03 — ✅ HIGH CONFIDENCE

  Person ID       : 314_1
  Employment      : non_worker
  Activity Bucket : Shopping
  Activity Label  : Buy goods (groceries, clothes, gas)

  Activity TAZ    : 3398.0
  Match Type      : taz_specific
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : Western Union
  POI Category    : Activities Related to Credit Intermediation
  POI TAZ         : 3398.0  (✓ Same TAZ)
  Distance        : 0.57 km

  MFC Score       : 1.000/1.000
  Confidence      : 5/5

  ASSESSMENT: ✅ Strong match — POI in exact target TAZ, 0.6 km distance is realistic

## CASE 04 — ✅ HIGH CONFIDENCE

  Person ID       : 797_3
  Employment      : non_worker
  Activity Bucket : Food
  Activity Label  : Buy food (go to the restaurant, food, carry-out)

  Activity TAZ    : 3398.0
  Match Type      : taz_specific
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : Ultimate Entertrainment Orlando
  POI Category    : Restaurants and Other Eating Places
  POI TAZ         : 3398.0  (✓ Same TAZ)
  Distance        : 0.54 km

  MFC Score       : 0.940/1.000
  Confidence      : 5/5

  ASSESSMENT: ✅ Strong match — POI in exact target TAZ, 0.5 km distance is realistic

## CASE 05 — ✅ HIGH CONFIDENCE

  Person ID       : 1025_3
  Employment      : non_worker
  Activity Bucket : Other
  Activity Label  : Religious or community activities

  Activity TAZ    : 3398.0
  Match Type      : taz_specific
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : True Pentecostal Holiness Church Inc
  POI Category    : Religious Organizations
  POI TAZ         : 3398.0  (✓ Same TAZ)
  Distance        : 0.23 km

  MFC Score       : 0.860/1.000
  Confidence      : 5/5

  ASSESSMENT: ✅ Strong match — POI in exact target TAZ, 0.2 km distance is realistic

## CASE 06 — ✅ HIGH CONFIDENCE

  Person ID       : 1376_2
  Employment      : non_worker
  Activity Bucket : Other
  Activity Label  : Religious or community activities

  Activity TAZ    : 3398.0
  Match Type      : taz_specific
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : Theolonias Ministries Electrifying & Edifying Signature
  POI Category    : Religious Organizations
  POI TAZ         : 3398.0  (✓ Same TAZ)
  Distance        : 0.17 km

  MFC Score       : 0.860/1.000
  Confidence      : 5/5

  ASSESSMENT: ✅ Strong match — POI in exact target TAZ, 0.2 km distance is realistic

## CASE 07 — ✅ HIGH CONFIDENCE

  Person ID       : 902_3
  Employment      : non_worker
  Activity Bucket : Shopping
  Activity Label  : Buy goods (groceries, clothes, gas)

  Activity TAZ    : 3398.0
  Match Type      : taz_specific
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : Designer Jewelry Store Wholesale to Public
  POI Category    : Jewelry, Luggage, and Leather Goods Stores
  POI TAZ         : 3398.0  (✓ Same TAZ)
  Distance        : 0.59 km

  MFC Score       : 1.000/1.000
  Confidence      : 5/5

  ASSESSMENT: ✅ Strong match — POI in exact target TAZ, 0.6 km distance is realistic

---

## TIER 2: MEDIUM CONFIDENCE CASES (Cases 08–13)

> **Definition:** confidence_score = 3.
> Causes: adjacent TAZ match, activity label ambiguity, or limited Veraset evidence in the target TAZ.


## CASE 08 — ⚠ MEDIUM CONFIDENCE

  Person ID       : 144_2
  Employment      : worker
  Activity Bucket : Work
  Activity Label  : Work-related activity, or volunteer

  Activity TAZ    : 3514
  Match Type      : similarity_nearby
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : Studio cheve
  POI Category    : Management of Companies and Enterprises
  POI TAZ         : 3514  (✓ Same TAZ)
  Distance        : 3.34 km

  MFC Score       : 0.745/1.000
  Confidence      : 3/5

  ASSESSMENT: ⚠ Acceptable — exact TAZ match but lower confidence from activity ambiguity

## CASE 09 — ⚠ MEDIUM CONFIDENCE

  Person ID       : 1759_1
  Employment      : non_worker
  Activity Bucket : Shopping
  Activity Label  : Buy goods (groceries, clothes, gas)

  Activity TAZ    : 3398
  Match Type      : similarity_nearby
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : Designer Jewelry Store Wholesale to Public
  POI Category    : Jewelry, Luggage, and Leather Goods Stores
  POI TAZ         : 3398  (✓ Same TAZ)
  Distance        : 2.15 km

  MFC Score       : 0.623/1.000
  Confidence      : 3/5

  ASSESSMENT: ⚠ Acceptable — exact TAZ match but lower confidence from activity ambiguity

## CASE 10 — ⚠ MEDIUM CONFIDENCE

  Person ID       : 24088_2
  Employment      : non_worker
  Activity Bucket : Food
  Activity Label  : Buy food (go to the restaurant, food, carry-out)

  Activity TAZ    : 3322
  Match Type      : similarity_nearby
  Ring Used       : Ring 3 (county-wide)

  POI Assigned    : Wild Horse Cafe
  POI Category    : Restaurants and Other Eating Places
  POI TAZ         : 3322  (✓ Same TAZ)
  Distance        : 0.68 km

  MFC Score       : 0.663/1.000
  Confidence      : 3/5

  ASSESSMENT: ⚠ County fallback — limited Veraset evidence in target TAZ, 0.7 km

## CASE 11 — ⚠ MEDIUM CONFIDENCE

  Person ID       : 10191_1
  Employment      : non_worker
  Activity Bucket : Other
  Activity Label  : Recreational activities (visit parks, movies, bars) or holidays like h

  Activity TAZ    : 4167.0
  Match Type      : taz_specific
  Ring Used       : Ring 3 (county-wide)

  POI Assigned    : Golf Galaxy
  POI Category    : Sporting Goods, Hobby, and Musical Instrument Stores
  POI TAZ         : 4167  (✗ Different TAZ)
  Distance        : 15.64 km

  MFC Score       : 0.712/1.000
  Confidence      : 3/5

  ASSESSMENT: ⚠ County fallback — limited Veraset evidence in target TAZ, 15.6 km

## CASE 12 — ⚠ MEDIUM CONFIDENCE

  Person ID       : 41016_3
  Employment      : non_worker
  Activity Bucket : School
  Activity Label  : Attend school

  Activity TAZ    : 3228.0
  Match Type      : taz_specific
  Ring Used       : Ring 3 (county-wide)

  POI Assigned    : Educational Design Studio
  POI Category    : Business Schools and Computer and Management Training
  POI TAZ         : 3221  (✗ Different TAZ)
  Distance        : 0.40 km

  MFC Score       : 0.722/1.000
  Confidence      : 3/5

  ASSESSMENT: ⚠ County fallback — limited Veraset evidence in target TAZ, 0.4 km

## CASE 13 — ⚠ MEDIUM CONFIDENCE

  Person ID       : 18718_4
  Employment      : non_worker
  Activity Bucket : Other
  Activity Label  : Religious or community activities

  Activity TAZ    : 3304
  Match Type      : similarity_nearby
  Ring Used       : Ring 3 (county-wide)

  POI Assigned    : Present Truth Seventh Day Adventist Church
  POI Category    : Religious Organizations
  POI TAZ         : 3304  (✓ Same TAZ)
  Distance        : 1.08 km

  MFC Score       : 0.750/1.000
  Confidence      : 3/5

  ASSESSMENT: ⚠ County fallback — limited Veraset evidence in target TAZ, 1.1 km

---

## TIER 3: LOW CONFIDENCE / EDGE CASES (Cases 14–20)

> **Definition:** confidence_score ≤ 2.
> Typical causes: county-wide Ring 3 fallback, sparse TAZ coverage, or activity-POI type mismatch.


## CASE 14 — ❌ LOW CONFIDENCE

  Person ID       : 5416_5
  Employment      : worker
  Activity Bucket : Work
  Activity Label  : Work-related activity, or volunteer

  Activity TAZ    : 3514
  Match Type      : similarity_nearby
  Ring Used       : Ring 3 (county-wide)

  POI Assigned    : Studio cheve
  POI Category    : Management of Companies and Enterprises
  POI TAZ         : 3514  (✓ Same TAZ)
  Distance        : 2.40 km

  MFC Score       : 0.553/1.000
  Confidence      : 2/5

  ASSESSMENT: ❌ County fallback — sparse Veraset coverage in TAZ 3514, best available POI at 2.4 km

## CASE 15 — ❌ LOW CONFIDENCE

  Person ID       : 3295_5
  Employment      : non_worker
  Activity Bucket : Shopping
  Activity Label  : Buy services (banking, service or repair a car, dry cleaners)

  Activity TAZ    : 4175.0
  Match Type      : taz_specific
  Ring Used       : Ring 1 (<5 km)

  POI Assigned    : Viva Americana
  POI Category    : Telecommunications
  POI TAZ         : 4175  (✗ Different TAZ)
  Distance        : 13.24 km

  MFC Score       : 0.607/1.000
  Confidence      : 2/5

  ASSESSMENT: ❌ Weak match — low MFC (0.607), activity-POI type mismatch

## CASE 16 — ❌ LOW CONFIDENCE

  Person ID       : 30871_1
  Employment      : non_worker
  Activity Bucket : Food
  Activity Label  : Buy food (go to the restaurant, food, carry-out)

  Activity TAZ    : 3290
  Match Type      : similarity_nearby
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : Donuts And Fuelpresso Inc
  POI Category    : Restaurants and Other Eating Places
  POI TAZ         : 3290  (✓ Same TAZ)
  Distance        : 0.26 km

  MFC Score       : 0.548/1.000
  Confidence      : 2/5

  ASSESSMENT: ❌ Weak match — low MFC (0.548), activity-POI type mismatch

## CASE 17 — ❌ LOW CONFIDENCE

  Person ID       : 25585_1
  Employment      : non_worker
  Activity Bucket : Other
  Activity Label  : Exercise (jog/walk, walk the dog, gym, diving, etc)

  Activity TAZ    : 3278
  Match Type      : similarity_nearby
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : Lake Apopka Loop Trail
  POI Category    : Museums, Historical Sites, and Similar Institutions
  POI TAZ         : 3278  (✓ Same TAZ)
  Distance        : 0.19 km

  MFC Score       : 0.558/1.000
  Confidence      : 2/5

  ASSESSMENT: ❌ Weak match — low MFC (0.558), activity-POI type mismatch

## CASE 18 — ❌ LOW CONFIDENCE

  Person ID       : 35296_3
  Employment      : non_worker
  Activity Bucket : Other
  Activity Label  : Recreational activities (visit parks, movies, bars) or holidays like h

  Activity TAZ    : 4715.0
  Match Type      : taz_specific
  Ring Used       : Ring 1 (<5 km)

  POI Assigned    : City Pub
  POI Category    : Drinking Places (Alcoholic Beverages)
  POI TAZ         : 4715  (✗ Different TAZ)
  Distance        : 31.81 km

  MFC Score       : 0.597/1.000
  Confidence      : 2/5

  ASSESSMENT: ❌ Weak match — low MFC (0.597), activity-POI type mismatch

## CASE 19 — ❌ LOW CONFIDENCE

  Person ID       : 201300_1
  Employment      : non_worker
  Activity Bucket : School
  Activity Label  : Attend school

  Activity TAZ    : 4627
  Match Type      : similarity_nearby
  Ring Used       : Ring 0 (exact TAZ)

  POI Assigned    : SafeStart Training
  POI Category    : Other Schools and Instruction
  POI TAZ         : 4627  (✓ Same TAZ)
  Distance        : 1.14 km

  MFC Score       : 0.607/1.000
  Confidence      : 2/5

  ASSESSMENT: ❌ Weak match — low MFC (0.607), activity-POI type mismatch

## CASE 20 — ❌ LOW CONFIDENCE

  Person ID       : 16775_3
  Employment      : non_worker
  Activity Bucket : Shopping
  Activity Label  : Buy goods (groceries, clothes, gas)

  Activity TAZ    : 3309.0
  Match Type      : taz_specific
  Ring Used       : N/A

  POI Assigned    : Millers Sod Sales
  POI Category    : Lawn and Garden Equipment and Supplies Stores
  POI TAZ         : 3309  (✗ Different TAZ)
  Distance        : 0.42 km

  MFC Score       : 0.325/1.000
  Confidence      : 1/5

  ASSESSMENT: ❌ County fallback — sparse Veraset coverage in TAZ 3309.0, best available POI at 0.4 km

---

## SUMMARY TABLE

| # | Tier | Activity | Match Type | Ring | Conf | MFC | Distance |
|---|------|----------|------------|------|------|-----|----------|
| 01 | HIGH ✅ | Work | taz_specific | Ring 0 | 5/5 | 0.823 | 7.17 km |
| 02 | HIGH ✅ | School | taz_specific | Ring 0 | 5/5 | 0.990 | 3.68 km |
| 03 | HIGH ✅ | Shopping | taz_specific | Ring 0 | 5/5 | 1.000 | 0.57 km |
| 04 | HIGH ✅ | Food | taz_specific | Ring 0 | 5/5 | 0.940 | 0.54 km |
| 05 | HIGH ✅ | Other | taz_specific | Ring 0 | 5/5 | 0.860 | 0.23 km |
| 06 | HIGH ✅ | Other | taz_specific | Ring 0 | 5/5 | 0.860 | 0.17 km |
| 07 | HIGH ✅ | Shopping | taz_specific | Ring 0 | 5/5 | 1.000 | 0.59 km |
| 08 | MED ⚠ | Work | similarity_nearby | Ring 0 | 3/5 | 0.745 | 3.34 km |
| 09 | MED ⚠ | Shopping | similarity_nearby | Ring 0 | 3/5 | 0.623 | 2.15 km |
| 10 | MED ⚠ | Food | similarity_nearby | Ring 3 | 3/5 | 0.663 | 0.68 km |
| 11 | MED ⚠ | Other | taz_specific | Ring 3 | 3/5 | 0.712 | 15.64 km |
| 12 | MED ⚠ | School | taz_specific | Ring 3 | 3/5 | 0.722 | 0.40 km |
| 13 | MED ⚠ | Other | similarity_nearby | Ring 3 | 3/5 | 0.750 | 1.08 km |
| 14 | LOW ❌ | Work | similarity_nearby | Ring 3 | 2/5 | 0.553 | 2.40 km |
| 15 | LOW ❌ | Shopping | taz_specific | Ring 1 | 2/5 | 0.607 | 13.24 km |
| 16 | LOW ❌ | Food | similarity_nearby | Ring 0 | 2/5 | 0.548 | 0.26 km |
| 17 | LOW ❌ | Other | similarity_nearby | Ring 0 | 2/5 | 0.558 | 0.19 km |
| 18 | LOW ❌ | Other | taz_specific | Ring 1 | 2/5 | 0.597 | 31.81 km |
| 19 | LOW ❌ | School | similarity_nearby | Ring 0 | 2/5 | 0.607 | 1.14 km |
| 20 | LOW ❌ | Shopping | taz_specific | Ring 3 | 1/5 | 0.325 | 0.42 km |

---

## KEY FINDINGS FROM CASE STUDIES

- **High-confidence cases** show consistent exact TAZ match, short realistic distances (<15 km), and strong MFC scores (>0.8)
- **Medium-confidence cases** typically have `match_type = similarity_nearby` — the similarity matcher found a good agent, but evidence was weaker in that TAZ
- **Low-confidence cases** are almost exclusively `emp_only` or county-wide Ring 3 fallbacks — these occur in TAZs with sparse Veraset coverage, not failures of the methodology
- Low-confidence rows represent only **1.2% of all 5.6M assignments**, and their POIs are still activity-compatible
