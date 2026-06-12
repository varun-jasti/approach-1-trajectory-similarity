# Visualizations

These figures were generated from the validated working-archive outputs.
Together they show assignment coverage, confidence and MFC quality,
distance-distribution comparisons, TAZ matching, activity composition, and
representative agent case studies.

Recommended starting points:

- `Distance_Distribution_Histogram.png`, `Distance_Percentiles.png` — authoritative
  distance metrics (median 0.853 km, matches `validation/distance_metrics.txt`
  and the README)
- `Confidence_distribution.png`
- `KS_Validation_DwellTime.png`, `KS_Validation_TimeOfDay.png`, `KS_Validation_Distance.png`
- `SyntheticVsReal_DistanceScatter.png`, `SyntheticVsReal_MatchQuality.png`
- `Case_study_examples.png`

## Figure-by-Figure Guide

Plain-language explanation of what each of the 18 figures shows.

### Distance & trip-length

- **`Distance_Distribution_Histogram.png`** — Histogram of how far (in km)
  each non-home activity is from the agent's home, across all 2.8M
  activities. Most trips are very short (under 1 km), with a long tail
  out to 50+ km. Vertical lines mark the median (0.85 km) and the
  75th/90th/95th percentiles.

- **`Distance_Percentiles.png`** — The same percentile values as a simple
  bar chart (median, 75th, 90th, 95th). It shows that 75% of all trips are
  under 3 km, and only 5% exceed about 19 km.

- **`trip_distance_bands.png`** — Compares the share of trips falling into
  distance "bands" (0-2 km, 2-5 km, etc.) for our synthetic agents vs. the
  real Veraset dataset (25.6M trips). Our agents take a larger share of
  very short (0-2 km) trips because POI matching is restricted to the
  Orange County area.

### Validation (KS tests)

- **`KS_Validation_Distance.png`** — A statistical (Kolmogorov-Smirnov)
  test comparing the shape of the distance distribution for synthetic vs.
  real Veraset agents. A KS p-value of 0.357 means the two distributions
  are statistically similar (PASS) — note the synthetic distances skew
  shorter due to the limited local POI scope.

- **`KS_Validation_DwellTime.png`** — Same KS test, but for how long agents
  stay at each activity (dwell time). A PASS result means the synthetic
  dwell-time pattern matches real behavior.

- **`KS_Validation_TimeOfDay.png`** — Same KS test, but for what time of
  day activities happen. PASS (p = 0.902), and both real and synthetic
  data peak around 7 PM, showing realistic daily rhythms.

### Quality and confidence scoring

- **`MFC_score_distribution.png`** — Histogram of the "Match Feasibility /
  Confidence" (MFC) quality score (0-1) for every assignment. Most
  assignments score near 1.0 ("Excellent"), with a vertical line marking
  the 0.8 "excellent" threshold.

- **`Confidence_distribution.png`** — Bar chart of the simple 1-5
  confidence rating given to each assignment. The vast majority (4.7M of
  5.6M) received the top score of 5, and almost none scored below 3.

### Activity and matching breakdown

- **`activity_distribution.png`** — Horizontal bar chart showing how many
  of the 5.6M assignments fall into each activity category. "Buy goods"
  (210K) and "Buy food" (142K) dominate, while categories like "Drop
  off/pick up someone" are rare.

- **`Match_Type_Distribution.png`** — Bar chart showing how each non-home
  activity got its location: 52.1% used an exact TAZ match, 46.7% used a
  nearby/similar zone, and only 1.2% fell back to an employment-only
  guess.

### Geographic / TAZ separation

- **`taz_separation.png`** — Shows that 76.7% of non-home activities happen
  in a different traffic zone (TAZ) than the agent's home, vs. 23.3%
  staying local — confirming agents genuinely travel across zones rather
  than clustering near home. This is the authoritative figure for the
  final dataset.

- **`TAZ_Match_Comparison.png`** — A 3-panel figure from an earlier,
  intermediate dataset (different row count/definition than the final
  results). It shows cross-zone travel (48.9%/51.1% — outdated, use
  `taz_separation.png` instead), POI assignment accuracy (86.3% land in
  the correct zone), and geographic realism (55.7% of POIs are outside the
  home zone).

### Synthetic vs. real comparison

- **`SyntheticVsReal_DistanceScatter.png`** — Scatter plot comparing each
  of 9 spot-checked synthetic agents' assignment distance (y-axis) against
  the real Veraset agent they were modeled after (x-axis). Points near the
  dashed diagonal line are a close match; points above it mean the
  synthetic agent traveled farther than its real counterpart.

- **`SyntheticVsReal_MatchQuality.png`** — For the same 9 spot-checked
  pairs, the left bar chart shows the absolute distance difference (km)
  between synthetic and real, and the right pie chart buckets these into
  Excellent/Good/Fair/Divergent. Overall average difference is 12.2 km on
  this small manual sample — this is an illustrative spot-check, not the
  full-dataset KS validation above.

### Case studies and archetypes

- **`Archetype_breakdown.png`** — Bar chart of how many of the 1.4M
  synthetic agents fall into each behavioral "archetype" (e.g.,
  LOCAL_RESIDENT, RECREATION_FOCUSED, COMMUTER_VISITOR). LOCAL_RESIDENT is
  the largest group at roughly 710,000 people.

- **`Case_study_examples.png`** — Three real example agents, one from each
  major archetype (LOCAL_COMMUTER, PARENT_CAREGIVER, LOCAL_RESIDENT),
  showing their dominant activity, median travel distance, MFC score, and
  confidence — all scoring perfectly (MFC 1.00, confidence 5/5).

### One-day agents and worker coverage

- **`OneDay_AgentRate.png`** — Compares the share of agents who only appear
  in the data for a single day. In the full Veraset dataset, 35.5% are
  "one-day" agents (likely tourists/one-time visitors), but only 6.0% of
  the agents actually used in this study are one-day, since the study
  filters to multi-day residents.

- **`OneDay_WorkerUndercount.png`** — Shows the impact of excluding those
  one-day agents on worker counts: 99.6% of workers are still correctly
  captured, with only 38 out of 638,158 study agents potentially missed —
  a negligible bias.

## Notes on specific figures

- **`KS_Validation_DwellTime.png`**, **`KS_Validation_TimeOfDay.png`**, and
  **`KS_Validation_Distance.png`** (split from a single combined figure) show
  the 3 core mobility-pattern KS tests (dwell time, time-of-day, distance),
  all of which PASS. Two additional tests (POI category mix, TAZ distribution)
  FAIL for reasons explained in `../validation/ks_test_full_results.txt` —
  read that file alongside these figures for the complete picture.

- **`SyntheticVsReal_DistanceScatter.png`** and **`SyntheticVsReal_MatchQuality.png`**
  (split from a single combined figure) show the per-pair distance comparison
  scatter plot and the distance-difference bar chart with match-quality pie
  chart, respectively.

- **`OneDay_AgentRate.png`** and **`OneDay_WorkerUndercount.png`** (split from
  a single combined figure) show the one-day agent exclusion rate and its
  negligible impact on worker coverage.

- **`taz_separation.png`** (76.7% cross-zone, matches the README and
  `validation/validation_report.md`) is the authoritative TAZ-separation
  figure for the final dataset. **`TAZ_Match_Comparison.png`**'s first panel
  reports a different figure (51.1%) computed on an earlier intermediate
  dataset (4,207,737-row "non-home" definition by activity_step rather than
  activity label) — its other two panels (POI assignment accuracy 86.3%,
  geographic realism 55.7%) are unique and still useful, but the 51.1%/48.9%
  split in the first panel should not be quoted as the headline cross-zone
  rate; use `taz_separation.png`'s 76.7% for that.
