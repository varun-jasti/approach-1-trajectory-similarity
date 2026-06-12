# Data Contract

Full source and result datasets are excluded because they are large and may be
licensed.

Included public files:

- `sample_data.csv`: 500 assignment rows for inspection and tests
- `trajectory_matching_sample_500.parquet`: equivalent Parquet sample
- `data_dictionary.md`: public output and simulation-export columns

## Synthetic Activity Rows

One row per synthetic person and activity:

| Column | Description |
|---|---|
| `person_id` | Synthetic person identifier |
| `activity` | Activity label |
| `home_taz` | Home traffic analysis zone |
| `home_lat`, `home_lon` | Synthetic home coordinates |
| `employment` | Employment class used for matching |

## Real-Agent Profiles

One row per real agent and observed activity:

| Column | Description |
|---|---|
| `caid` | De-identified real-agent identifier |
| `activity` | Activity label |
| `home_taz`, `home_lat`, `home_lon` | Real agent home geography |
| `activity_taz`, `activity_lat`, `activity_lon` | Observed activity geography |
| `employment` | Employment class |

## POIs

Required columns are `activity_label1`, `latitude`, and `longitude`. Optional
metadata columns are `SAFEGRAPH_PLACE_ID`, `LOCATION_NAME`, `TOP_CATEGORY`,
and `taz_id`.

## Full Data

The Veraset shards, synthetic population, full POI source, agent profiles, and
full assignment output are not distributed here. Contact the project authors
and comply with the applicable data agreements to obtain licensed inputs.
