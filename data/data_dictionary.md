# Data Dictionary

## Assignment Output

| Column | Description |
|---|---|
| `person_id` | Synthetic person identifier |
| `activity_step` / `step` | Position in the daily activity chain |
| `activity` | Assigned activity purpose |
| `matched_caid` | De-identified Veraset agent used for spatial matching |
| `match_type` | Exact-TAZ, similarity, or fallback matching method |
| `home_lat`, `home_lon`, `home_taz` | Synthetic person's home geography |
| `activity_taz` | Translated target activity zone |
| `poi_safegraph_id` / `safegraph_place_id` | Assigned POI identifier |
| `poi_name`, `poi_category` | Assigned POI metadata |
| `poi_lat`, `poi_lon`, `poi_taz` | Assigned POI geography |
| `distance_km` | Great-circle distance from home to POI |
| `mfc_score` | Multi-factor composite quality score from 0 to 1 |
| `confidence_score` | Assignment confidence score from 1 to 5 |
| `taz_ring_used` | Hierarchical geographic fallback ring |
