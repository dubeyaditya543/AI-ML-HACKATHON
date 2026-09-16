"""
MANGANEX — Feature Engineering Module
Computes spectral indices from Sentinel-2 band reflectance values
for mineral prospectivity mapping.
"""

import numpy as np
import pandas as pd


def compute_ndvi(nir, red):
    """
    Normalized Difference Vegetation Index.
    Low NDVI indicates barren/mineral-rich terrain.

    Formula: (B8 - B4) / (B8 + B4)
    """
    return (nir - red) / (nir + red + 1e-10)


def compute_clay_index(swir1, swir2):
    """
    Clay Mineral Ratio.
    High values indicate clay-rich alteration zones
    often associated with mineral deposits.

    Formula: B11 / B12
    """
    return swir1 / (swir2 + 1e-10)


def compute_ferrous_index(swir1, nir):
    """
    Ferrous Minerals Index.
    Highlights iron and manganese-bearing minerals.

    Formula: B11 / B8
    """
    return swir1 / (nir + 1e-10)


def compute_mn_proxy(swir1, swir2):
    """
    Manganese Proxy Index — custom spectral ratio
    sensitive to manganese-related spectral anomalies.

    Formula: (B11 - B12) / (B11 + B12)
    """
    return (swir1 - swir2) / (swir1 + swir2 + 1e-10)


def compute_iron_oxide_index(red, blue):
    """
    Iron Oxide Index.
    Highlights iron oxide minerals (goethite, hematite)
    which often co-occur with manganese deposits.

    Formula: B4 / B2
    """
    return red / (blue + 1e-10)


def compute_all_features(df):
    """
    Compute all spectral indices from a DataFrame containing
    Sentinel-2 band values.

    Expected columns: B2, B3, B4, B8, B11, B12

    Returns:
        DataFrame with added spectral index columns
    """
    result = df.copy()

    # Spectral indices
    result["ndvi"] = compute_ndvi(df["B8"], df["B4"])
    result["clay_index"] = compute_clay_index(df["B11"], df["B12"])
    result["ferrous_index"] = compute_ferrous_index(df["B11"], df["B8"])
    result["mn_proxy"] = compute_mn_proxy(df["B11"], df["B12"])
    result["iron_oxide_index"] = compute_iron_oxide_index(df["B4"], df["B2"])

    # Derived features
    result["swir_ratio"] = df["B11"] / (df["B12"] + 1e-10)
    result["nir_swir_diff"] = df["B8"] - df["B11"]
    result["spectral_variability"] = df[["B2", "B3", "B4", "B8", "B11", "B12"]].std(axis=1)

    return result


def get_feature_columns():
    """Return the list of feature column names used for ML training."""
    return [
        "ndvi", "clay_index", "ferrous_index", "mn_proxy",
        "iron_oxide_index", "swir_ratio", "nir_swir_diff",
        "spectral_variability",
        "elevation", "slope", "distance_to_fault",
        "B2", "B3", "B4", "B8", "B11", "B12",
    ]


def normalize_features(df, feature_cols=None):
    """
    Min-max normalize features to [0, 1] range.
    Returns normalized DataFrame and the min/max values for inverse transform.
    """
    if feature_cols is None:
        feature_cols = get_feature_columns()

    cols_present = [c for c in feature_cols if c in df.columns]
    result = df.copy()

    stats = {}
    for col in cols_present:
        min_val = df[col].min()
        max_val = df[col].max()
        range_val = max_val - min_val
        if range_val > 0:
            result[col] = (df[col] - min_val) / range_val
        else:
            result[col] = 0.0
        stats[col] = {"min": min_val, "max": max_val}

    return result, stats
