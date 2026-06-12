"""Generate a validation report for an assignment output."""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
subprocess.run(
    [
        sys.executable,
        str(ROOT / "code/03_validation.py"),
        "--assignments", "output/assignments.parquet",
        "--output", "output/validation_report.json",
    ],
    check=True,
)
