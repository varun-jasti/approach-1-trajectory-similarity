"""Template for launching a full-size production assignment run."""

from pathlib import Path


PROJECT = Path("/path/to/Veraset_Data")
COMMAND = [
    "python3",
    "code/01_trajectory_matching.py",
    "--synthetic", str(PROJECT / "synthetic_activity_rows.parquet"),
    "--profiles", str(PROJECT / "agent_trajectory_profiles.parquet"),
    "--pois", str(PROJECT / "poi_with_activity_labels.parquet"),
    "--output", str(PROJECT / "output/A3_final.parquet"),
]

print("Configure PROJECT, then run:")
print(" ".join(COMMAND))
