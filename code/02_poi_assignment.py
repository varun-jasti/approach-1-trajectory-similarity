"""Assign nearest activity-compatible POIs to translated trajectory targets."""

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from utils import haversine_km


def assign_pois(matches: pd.DataFrame, pois: pd.DataFrame) -> pd.DataFrame:
    """Assign the nearest compatible POI for every matched activity row."""
    required = {"activity", "target_lat", "target_lon"}
    missing = required - set(matches.columns)
    if missing:
        raise ValueError(f"Matches are missing columns: {sorted(missing)}")

    pois = pois.rename(
        columns={
            "activity_label1": "activity",
            "latitude": "poi_lat",
            "longitude": "poi_lon",
            "taz_id": "poi_taz",
            "SAFEGRAPH_PLACE_ID": "safegraph_place_id",
            "LOCATION_NAME": "poi_name",
            "TOP_CATEGORY": "poi_category",
        }
    ).copy()
    for column in ["safegraph_place_id", "poi_name", "poi_category", "poi_taz"]:
        if column not in pois:
            pois[column] = pd.NA
    pois["activity_key"] = pois["activity"].astype(str).str.lower().str.strip()

    result = matches.copy()
    result["activity_key"] = result["activity"].astype(str).str.lower().str.strip()
    output_columns = ["safegraph_place_id", "poi_name", "poi_category", "poi_lat", "poi_lon", "poi_taz"]
    for column in output_columns:
        result[column] = np.nan if column in {"poi_lat", "poi_lon"} else pd.NA

    for activity, indices in result.groupby("activity_key").groups.items():
        candidates = pois[pois["activity_key"] == activity].reset_index(drop=True)
        if candidates.empty:
            continue
        tree = cKDTree(candidates[["poi_lat", "poi_lon"]].to_numpy())
        query = result.loc[indices, ["target_lat", "target_lon"]].to_numpy()
        _, nearest = tree.query(query, k=1)
        selected = candidates.iloc[nearest].reset_index(drop=True)
        for column in output_columns:
            result.loc[indices, column] = selected[column].to_numpy()

    assigned = result["poi_lat"].notna()
    result["distance_km"] = np.nan
    result.loc[assigned, "distance_km"] = haversine_km(
        result.loc[assigned, "home_lat"],
        result.loc[assigned, "home_lon"],
        result.loc[assigned, "poi_lat"],
        result.loc[assigned, "poi_lon"],
    )
    return result.drop(columns="activity_key")
