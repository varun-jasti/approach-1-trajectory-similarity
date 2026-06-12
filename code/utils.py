"""Shared geographic and data-loading utilities."""

from pathlib import Path

import numpy as np
import pandas as pd


def read_table(path: str | Path, columns: list[str] | None = None) -> pd.DataFrame:
    """Read a CSV or Parquet table."""
    path = Path(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, usecols=columns)
    if path.suffix.lower() in {".parquet", ".pq"}:
        return pd.read_parquet(path, columns=columns)
    raise ValueError(f"Unsupported table format: {path.suffix}")


def normalize_taz(value: object) -> str | None:
    """Normalize numeric-looking TAZ values to comparable strings."""
    try:
        return str(int(float(value)))
    except (TypeError, ValueError):
        return None


def haversine_km(lat1, lon1, lat2, lon2):
    """Return great-circle distance in kilometers; inputs may be arrays."""
    lat1, lon1, lat2, lon2 = map(np.asarray, (lat1, lon1, lat2, lon2))
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(np.radians(lat1))
        * np.cos(np.radians(lat2))
        * np.sin(dlon / 2) ** 2
    )
    return 6371.0 * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


def translated_target(home_lat, home_lon, real_home_lat, real_home_lon, real_lat, real_lon):
    """Translate a real activity's relative displacement to a synthetic home."""
    return home_lat + real_lat - real_home_lat, home_lon + real_lon - real_home_lon
