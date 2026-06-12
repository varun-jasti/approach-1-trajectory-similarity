#!/usr/bin/env python3
"""Validate basic quality properties of the included public sample."""

from pathlib import Path

import pandas as pd


sample = Path(__file__).parents[1] / "data" / "sample_data.csv"
rows = pd.read_csv(sample)

required = {"person_id", "activity", "poi_lat", "poi_lon", "distance_km", "confidence_score"}
missing = required - set(rows.columns)
assert not missing, f"Missing required columns: {sorted(missing)}"
assert rows[["poi_lat", "poi_lon"]].notna().all().all(), "Sample contains missing POI coordinates"
assert rows["distance_km"].ge(0).all(), "Sample contains negative distances"
assert rows["confidence_score"].between(1, 5).all(), "Confidence must be between 1 and 5"

print(f"Validated {len(rows):,} sample assignment rows.")
