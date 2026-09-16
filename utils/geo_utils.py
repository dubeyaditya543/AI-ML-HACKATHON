"""
MANGANEX — Geospatial Utility Functions
Helper functions for coordinate transformations, distance calculations, and GeoJSON generation.
"""

import math
import numpy as np
import pandas as pd


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points
    on Earth using the Haversine formula.

    Args:
        lat1, lon1: Coordinates of point 1 (degrees)
        lat2, lon2: Coordinates of point 2 (degrees)

    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in km

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def generate_grid(lat_min, lat_max, lon_min, lon_max, step=0.1):
    """
    Generate a regular grid of latitude/longitude points.

    Args:
        lat_min, lat_max: Latitude bounds
        lon_min, lon_max: Longitude bounds
        step: Grid spacing in degrees (default 0.1° ≈ 11km)

    Returns:
        DataFrame with 'latitude' and 'longitude' columns
    """
    lats = np.arange(lat_min, lat_max, step)
    lons = np.arange(lon_min, lon_max, step)
    grid = np.array(np.meshgrid(lats, lons)).T.reshape(-1, 2)

    return pd.DataFrame(grid, columns=["latitude", "longitude"])


def points_to_geojson(df, lat_col="latitude", lon_col="longitude", properties_cols=None):
    """
    Convert a DataFrame of points to GeoJSON FeatureCollection.

    Args:
        df: DataFrame with coordinate columns
        lat_col: Name of latitude column
        lon_col: Name of longitude column
        properties_cols: List of column names to include as feature properties

    Returns:
        GeoJSON dict
    """
    if properties_cols is None:
        properties_cols = [c for c in df.columns if c not in [lat_col, lon_col]]

    features = []
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row[lon_col], row[lat_col]],
            },
            "properties": {col: row[col] for col in properties_cols if col in row.index},
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features,
    }


def get_bounding_box(df, lat_col="latitude", lon_col="longitude", padding=0.5):
    """
    Get the bounding box of a set of points with optional padding.

    Returns:
        Tuple of (lat_min, lat_max, lon_min, lon_max)
    """
    return (
        df[lat_col].min() - padding,
        df[lat_col].max() + padding,
        df[lon_col].min() - padding,
        df[lon_col].max() + padding,
    )


def format_coordinates(lat, lon, precision=4):
    """Format coordinates as a readable string."""
    lat_dir = "N" if lat >= 0 else "S"
    lon_dir = "E" if lon >= 0 else "W"
    return f"{abs(lat):.{precision}f}°{lat_dir}, {abs(lon):.{precision}f}°{lon_dir}"
