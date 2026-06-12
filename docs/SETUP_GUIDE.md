# Setup Guide

## Install

```bash
git clone https://github.com/YOUR_USERNAME/approach-1-trajectory-similarity.git
cd approach-1-trajectory-similarity
python3 -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
```

## Run the Portable Pipeline

```bash
python3 code/01_trajectory_matching.py \
  --synthetic path/to/synthetic_activity_rows.parquet \
  --profiles path/to/real_agent_profiles.parquet \
  --pois path/to/activity_labelled_pois.parquet \
  --output output/assignments.parquet

python3 code/03_validation.py \
  --assignments output/assignments.parquet \
  --output output/validation_report.json
```

## Production Scripts

`code/production/` contains the original research scripts used for the
large-scale run. They preserve project-specific paths and historical `A3_*`
output names for reproducibility. Review and configure their path constants
before running them on another machine.

## Data Availability

Licensed Veraset, synthetic-population, and full POI inputs are not distributed
in this repository. The full `A3_final.parquet` result is also excluded because
it exceeds GitHub's 100 MB per-file limit. Use Git LFS or an institutional data
repository when distributing full outputs.
