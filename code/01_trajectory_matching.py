#!/usr/bin/env python3
"""Run trajectory-similarity matching and POI assignment."""

import argparse
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from utils import normalize_taz, read_table, translated_target


def _load_poi_module():
    path = Path(__file__).with_name("02_poi_assignment.py")
    spec = importlib.util.spec_from_file_location("poi_assignment", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def match_agents(synthetic: pd.DataFrame, profiles: pd.DataFrame) -> pd.DataFrame:
    """Match by exact home TAZ/employment, then nearest same-employment home."""
    synthetic = synthetic.copy()
    profiles = profiles.copy()
    for frame in (synthetic, profiles):
        frame["home_taz_key"] = frame["home_taz"].map(normalize_taz)
        frame["activity_key"] = frame["activity"].astype(str).str.lower().str.strip()

    exact = profiles.drop_duplicates(["home_taz_key", "employment", "activity_key"])
    matched = synthetic.merge(
        exact,
        on=["home_taz_key", "employment", "activity_key"],
        how="left",
        suffixes=("", "_real"),
    )
    matched["match_type"] = np.where(matched["caid"].notna(), "taz_employment", None)

    unmatched = matched[matched["caid"].isna()]
    for (employment, activity), indices in unmatched.groupby(["employment", "activity_key"]).groups.items():
        candidates = profiles[
            (profiles["employment"] == employment) & (profiles["activity_key"] == activity)
        ].reset_index(drop=True)
        if candidates.empty:
            continue
        tree = cKDTree(candidates[["home_lat", "home_lon"]].to_numpy())
        _, nearest = tree.query(matched.loc[indices, ["home_lat", "home_lon"]].to_numpy(), k=1)
        selected = candidates.iloc[nearest].reset_index(drop=True)
        for column in ["caid", "home_lat", "home_lon", "activity_lat", "activity_lon", "activity_taz"]:
            target = f"{column}_real" if column in matched.columns else column
            if column in selected.columns:
                matched.loc[indices, target] = selected[column].to_numpy()
        matched.loc[indices, "match_type"] = "nearest_employment"

    matched["matched_caid"] = matched["caid"]
    matched[["target_lat", "target_lon"]] = matched.apply(
        lambda row: translated_target(
            row["home_lat"],
            row["home_lon"],
            row["home_lat_real"],
            row["home_lon_real"],
            row["activity_lat"],
            row["activity_lon"],
        ),
        axis=1,
        result_type="expand",
    )
    return matched


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--synthetic", required=True)
    parser.add_argument("--profiles", required=True)
    parser.add_argument("--pois", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    synthetic = read_table(args.synthetic)
    profiles = read_table(args.profiles)
    pois = read_table(args.pois)
    matches = match_agents(synthetic, profiles)
    assignments = _load_poi_module().assign_pois(matches, pois)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    assignments.to_parquet(output, index=False)
    print(f"Wrote {len(assignments):,} assignments to {output}")


if __name__ == "__main__":
    main()
