"""Minimal command-line invocation of the portable pipeline."""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
subprocess.run(
    [
        sys.executable,
        str(ROOT / "code/01_trajectory_matching.py"),
        "--synthetic", "path/to/synthetic_activity_rows.parquet",
        "--profiles", "path/to/real_agent_profiles.parquet",
        "--pois", "path/to/activity_labelled_pois.parquet",
        "--output", "output/assignments.parquet",
    ],
    check=True,
)
