"""
MANGANEX — Google Earth Engine Sentinel-2 Data Fetcher
Standalone script for fetching satellite imagery from GEE.

Prerequisites:
    1. pip install earthengine-api geemap
    2. Run `earthengine authenticate` once
    3. Create a GEE project at https://code.earthengine.google.com/

Usage:
    python gee/sentinel_fetcher.py

Note: The main MANGANEX app works without this script using synthetic data.
This is provided for fetching real satellite data when GEE access is available.
"""

import os
import sys
import pandas as pd
import numpy as np

try:
    import ee
    GEE_AVAILABLE = True
except ImportError:
    GEE_AVAILABLE = False
    print("⚠️  earthengine-api not installed. Install with: pip install earthengine-api")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import MANGANESE_BELTS, SENTINEL2_BANDS

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def initialize_gee(project_id=None):
    """Initialize Google Earth Engine."""
    if not GEE_AVAILABLE:
        print("❌ earthengine-api not available.")
        return False

    try:
        if project_id:
            ee.Initialize(project=project_id)
        else:
            ee.Initialize()
        print("✅ Google Earth Engine initialized successfully.")
        return True
    except Exception as e:
        print(f"❌ GEE initialization failed: {e}")
        print("   Run 'earthengine authenticate' first.")
        return False


def get_sentinel2_composite(aoi, start_date, end_date, cloud_threshold=20):
    """
    Fetch a cloud-free Sentinel-2 L2A composite for an area of interest.

    Args:
        aoi: ee.Geometry defining the area of interest
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        cloud_threshold: Maximum cloud cover percentage

    Returns:
        ee.Image: Median composite of filtered collection
    """
    # Load Sentinel-2 Surface Reflectance collection
    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_threshold))
    )

    # Cloud masking function using SCL band
    def mask_clouds(image):
        scl = image.select("SCL")
        # Keep vegetation, bare soil, water (classes 4, 5, 6, 7)
        mask = scl.gte(4).And(scl.lte(7))
        return image.updateMask(mask).divide(10000)

    # Apply cloud mask and create median composite
    composite = collection.map(mask_clouds).median()

    # Select required bands
    bands = list(SENTINEL2_BANDS.keys())
    composite = composite.select(bands)

    print(f"📡 Fetched Sentinel-2 composite: {collection.size().getInfo()} images")
    return composite


def extract_band_values(composite, points, scale=20):
    """
    Extract band values at specific point locations.

    Args:
        composite: ee.Image with band values
        points: List of (lat, lon) tuples
        scale: Spatial resolution in meters

    Returns:
        List of dicts with band values for each point
    """
    results = []

    for lat, lon in points:
        point = ee.Geometry.Point(lon, lat)
        values = composite.sample(point, scale).first()

        if values:
            info = values.getInfo()
            if info and "properties" in info:
                results.append({
                    "latitude": lat,
                    "longitude": lon,
                    **info["properties"]
                })

    return results


def fetch_elevation_data(aoi):
    """
    Fetch SRTM elevation and compute slope for an area of interest.

    Returns:
        Tuple of (elevation_image, slope_image)
    """
    dem = ee.Image("USGS/SRTMGL1_003")
    elevation = dem.select("elevation").clip(aoi)
    slope = ee.Terrain.slope(dem).clip(aoi)

    return elevation, slope


def fetch_data_for_belt(state_name, start_date="2023-01-01", end_date="2023-12-31"):
    """
    Fetch satellite data for a specific manganese belt.

    Args:
        state_name: Name of the state (must match MANGANESE_BELTS keys)
        start_date: Start date for imagery
        end_date: End date for imagery

    Returns:
        DataFrame with band values for a grid of points
    """
    if state_name not in MANGANESE_BELTS:
        print(f"❌ Unknown state: {state_name}")
        return None

    belt = MANGANESE_BELTS[state_name]
    lat_center, lon_center = belt["center"]

    # Create AOI (1.5° x 1.5° bounding box around belt center)
    aoi = ee.Geometry.Rectangle(
        [lon_center - 1.5, lat_center - 1.5,
         lon_center + 1.5, lat_center + 1.5]
    )

    print(f"\n🛰️  Fetching data for {state_name} belt...")
    print(f"   Center: {lat_center}°N, {lon_center}°E")
    print(f"   Date range: {start_date} to {end_date}")

    # Get Sentinel-2 composite
    composite = get_sentinel2_composite(aoi, start_date, end_date)

    # Generate sample points
    grid_step = 0.05  # ~5.5km spacing
    points = [
        (lat_center + dlat, lon_center + dlon)
        for dlat in np.arange(-1.5, 1.5, grid_step)
        for dlon in np.arange(-1.5, 1.5, grid_step)
    ]

    print(f"   Extracting values for {len(points)} grid points...")

    # Extract band values
    band_data = extract_band_values(composite, points)

    if band_data:
        df = pd.DataFrame(band_data)
        df["state"] = state_name
        print(f"   ✅ Extracted {len(df)} points with valid data")
        return df
    else:
        print("   ⚠️ No valid data extracted")
        return None


def main():
    """Fetch satellite data for all manganese belts."""
    print("=" * 60)
    print("  MANGANEX — GEE Sentinel-2 Data Fetcher")
    print("=" * 60)

    if not initialize_gee():
        print("\n💡 To use real satellite data:")
        print("   1. pip install earthengine-api")
        print("   2. earthengine authenticate")
        print("   3. Re-run this script")
        print("\n   The app will use synthetic data in the meantime.")
        return

    all_data = []

    for state_name in MANGANESE_BELTS:
        df = fetch_data_for_belt(state_name)
        if df is not None:
            all_data.append(df)

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        output_path = os.path.join(DATA_DIR, "sentinel2_real_data.csv")
        combined.to_csv(output_path, index=False)
        print(f"\n✅ Saved {len(combined)} records → {output_path}")
    else:
        print("\n⚠️ No data was fetched. Check GEE authentication.")


if __name__ == "__main__":
    main()
