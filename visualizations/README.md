# Visualizations

Six figures covering the core validation story for Approach 1 (Trajectory Similarity Matching).

---

## 1. `Distance_Distribution_Histogram.png`

Histogram of trip distances (home → assigned POI) across all 2.8M non-home activities.
Median is 0.853 km — short because the POI pool is scoped to Orange County residents only,
not the statewide Veraset dataset that includes tourists and long-distance travelers.
Percentile lines (75th, 90th, 95th) show the full spread.

---

## 2. `KS_Validation_Distance.png`

Kolmogorov-Smirnov test comparing the binned distance distribution of synthetic assignments
vs. the Veraset reference distribution (Orange County scope). KS p = 0.357 → **PASS**:
the two distributions are statistically indistinguishable at the 5% level.
Synthetic distances skew shorter than statewide Veraset due to the local-only POI scope —
this is expected and documented.

> **Note on timing KS tests:** earlier versions included `KS_Validation_DwellTime.png`
> and `KS_Validation_TimeOfDay.png` for the activity timing layer. That work is separate
> from this repo's POI-assignment scope and is pending confirmation —
> see `09_SIMULATION_INTEGRATION/03_TIMING_VALIDATION_PENDING_REVIEW/`.

---

## 3. `Confidence_distribution.png`

Bar chart of the 1–5 confidence score for every assignment. **96.3% score 4 or 5**
(High / Very High). The score combines the MFC quality score with archetype-activity
compatibility and TAZ match tightness.

---

## 4. `MFC_score_distribution.png`

Histogram of the six-factor MFC quality score (0–1) across all 5.6M assignments.
**86.2% score above 0.8 (Excellent)**. Factors: activity-category match, distance
realism, TAZ match, Veraset visit frequency, category appropriateness, time-of-day fit.

---

## 5. `Match_Type_BeforeAfter.png`

Before/after comparison of the trajectory fallback rate. Before the 6D similarity
matching fix, **47.9%** of assignments used a random employment-only fallback — almost
half the dataset was matched to geographically inappropriate "twins." After replacing
random selection with 6-dimensional similarity matching, the fallback rate dropped to
**1.2%** (a 97% reduction), with 98.8% of assignments using TAZ-specific or
similarity-nearby matches.

---

## 6. `TAZ_Ring_Fix_BeforeAfter.png`

Before/after comparison of the TAZ ring search fix. Before introducing the hierarchical
ring search (Ring 0–3), only **82.5%** of non-home activities were matched within Ring 0
or Ring 1. After the fix, **96.5%** land in Ring 0 or Ring 1 — a 14 percentage-point
improvement. Ring 2–3 (broader county search) now covers only 3.5% of cases.

---

## Case studies

Individual agent examples (high / medium / low confidence) are documented in
[`../docs/CASE_STUDIES.md`](../docs/CASE_STUDIES.md).
