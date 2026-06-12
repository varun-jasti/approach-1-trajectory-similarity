#!/usr/bin/env python3
"""Generate a compact JSON quality report for POI assignments."""

import argparse
import json
from pathlib import Path

from utils import read_table


def validation_metrics(assignments):
    """Calculate assignment coverage, distance, and confidence metrics."""
    assigned = assignments["poi_lat"].notna() & assignments["poi_lon"].notna()
    metrics = {
        "rows": int(len(assignments)),
        "successful_assignments": int(assigned.sum()),
        "success_rate": float(assigned.mean()),
        "unique_pois": int(assignments.loc[assigned, "safegraph_place_id"].nunique()),
        "median_distance_km": float(assignments.loc[assigned, "distance_km"].median()),
        "mean_distance_km": float(assignments.loc[assigned, "distance_km"].mean()),
    }
    if "confidence_score" in assignments:
        metrics["mean_confidence"] = float(assignments["confidence_score"].mean())
        metrics["high_confidence_rate"] = float(assignments["confidence_score"].ge(4).mean())
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assignments", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    metrics = validation_metrics(read_table(args.assignments))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
