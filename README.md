# Approach 1: Trajectory Similarity Matching for POI Assignment

Complete implementation and research artifacts for assigning real-world points
of interest (POIs) to 1.4 million synthetic travel agents using trajectory
similarity matching on Veraset GPS mobility data.

## Key Results

| Metric | Value |
|---|---:|
| Synthetic agents | 1,402,579 |
| Activity rows | 5,610,316 |
| Successful assignments | **99.84%** |
| Assigned unique POIs | 49,157 |
| Simulation POI lookup | 55,717 |
| Median non-home distance | **0.85 km** |
| Mean confidence | **4.79 / 5** |
| High confidence (4-5) | 96.3% |



## Visualizations — Where to Start

For a quick understanding of the results, view these figures in order:

1. [`Distance_Distribution_Histogram.png`](visualizations/Distance_Distribution_Histogram.png) — confirms the 0.85 km median trip distance
2. [`Confidence_distribution.png`](visualizations/Confidence_distribution.png) — shows 96.3% of assignments are high confidence
3. [`KS_Validation_DwellTime.png`](visualizations/KS_Validation_DwellTime.png), [`KS_Validation_TimeOfDay.png`](visualizations/KS_Validation_TimeOfDay.png), [`KS_Validation_Distance.png`](visualizations/KS_Validation_Distance.png) — behavioral pattern validation against real Veraset data (all PASS)
4. [`Archetype_breakdown.png`](visualizations/Archetype_breakdown.png) — population diversity across behavioral archetypes
5. [`Case_study_examples.png`](visualizations/Case_study_examples.png) — real example assignments

For the full figure guide, including notes on which figures are authoritative
and known caveats, see [`visualizations/README.md`](visualizations/README.md).

## Method

1. Match each synthetic person to a real Veraset agent using home TAZ,
   employment class, activity type, and similarity fallback.
2. Transfer the real agent's relative activity trajectory to the synthetic
   person's home geography.
3. Assign the nearest activity-compatible POI using hierarchical geographic
   fallback.
4. Validate coverage, distances, TAZ separation, confidence, POI diversity,
   and distribution similarity.

```text
target_activity_location =
    synthetic_home + (real_activity_location - real_home)
```

## Repository Contents

| Folder | Contents |
|---|---|
| `code/` | Portable pipeline plus original production scripts |
| `data/` | Public CSV/Parquet samples and data dictionary |
| `results/` | POI lookup, example output, and summary metrics |
| `validation/` | KS tests, reports, metric summaries, and sample checks |
| `docs/` | Method, setup, paper draft, case studies, and integration notes |
| `visualizations/` | Validation and results figures |
| `examples/` | Portable usage templates |

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/approach-1-trajectory-similarity.git
cd approach-1-trajectory-similarity
python3 -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
```

Run the portable pipeline:

```bash
python3 code/01_trajectory_matching.py \
  --synthetic path/to/synthetic_activity_rows.parquet \
  --profiles path/to/agent_trajectory_profiles.parquet \
  --pois path/to/activity_labelled_pois.parquet \
  --output output/assignments.parquet

python3 code/03_validation.py \
  --assignments output/assignments.parquet \
  --output output/validation_report.json
```

The original large-scale research scripts are preserved in `code/production/`.
They contain project-specific paths and should be configured before execution.

## Included Data and Results

- `data/sample_data.csv`: 500-row public output sample
- `data/trajectory_matching_sample_500.parquet`: Parquet version of the sample
- `results/poi_lookup.parquet`: actual 55,717-row simulation POI lookup
- `results/sample_output.csv`: representative assignment output
- `results/summary_statistics.json`: validated headline metrics

The full output and licensed source data are not included.
Final output is approximately 135 MB, above GitHub's ordinary 100 MB
per-file limit. Use Git LFS or an institutional data repository for full-data
distribution.

## Documentation

- [Setup guide](docs/SETUP_GUIDE.md)
- [Method](docs/METHOD.md)
- [Results summary](docs/RESULTS_SUMMARY.md)
- [Validation report](validation/validation_report.md)
- [Full KS distribution test results (incl. known limitations)](validation/ks_test_full_results.txt)
- [Technical paper draft](docs/TECHNICAL_PAPER_DRAFT.md)
- [Data dictionary](data/data_dictionary.md)

## Reading Order for Reviewers

**5-minute overview**
- This README
- [`visualizations/Distance_Distribution_Histogram.png`](visualizations/Distance_Distribution_Histogram.png)
- [`results/summary_statistics.json`](results/summary_statistics.json)

**15-minute validation check**
- [Validation report](validation/validation_report.md)
- [`visualizations/KS_Validation_*.png`](visualizations/) (3 files)
- [`validation/confidence_metrics.txt`](validation/confidence_metrics.txt)

**Full understanding**
- [Method](docs/METHOD.md)
- [`validation/taz_fix_validation.txt`](validation/taz_fix_validation.txt)
- All figures in [`visualizations/`](visualizations/)

## Authors

- Professor Xishun Liao, University of Central Florida
- Viswanadh Jasti, University of Central Florida


## License and Citation

Code and documentation are available under the [MIT License](LICENSE). Source
mobility and POI datasets remain subject to their original licenses. Citation
metadata is provided in [CITATION.cff](CITATION.cff).
