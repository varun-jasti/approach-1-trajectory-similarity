# Code Implementation

## Portable Pipeline

- `01_trajectory_matching.py`: match agents, translate trajectories, and run
  POI assignment
- `02_poi_assignment.py`: nearest activity-compatible POI lookup
- `03_validation.py`: JSON validation report generation
- `utils.py`: geographic and table-loading helpers

## Production Research Scripts

`production/` contains the actual scripts used during the research workflow:

- `similarity_matching_production.py`
- `taz_offset_production.py`

These preserve historical `A3_*` output names and machine-specific path
constants for reproducibility. Configure paths before running them elsewhere.

## Running

Run commands from the repository root:

```bash
pip install -r code/requirements.txt
python3 code/01_trajectory_matching.py --help
python3 code/03_validation.py --help
```

The portable scripts accept CSV or Parquet inputs. Generated full outputs
should remain outside ordinary Git.
