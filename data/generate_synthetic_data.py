"""
MANGANEX — Synthetic Data Generator
Generates realistic demo datasets for manganese exploration across India's known mineral belts.
Run this script once to populate the data/ directory.

Usage:
    python data/generate_synthetic_data.py
"""

import os
import sys
import numpy as np
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import MANGANESE_BELTS, PRODUCTION_YEARS

np.random.seed(42)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_deposit_data():
    """
    Generate ~120 known manganese deposit locations across India's major belts.
    Each deposit has coordinates, grade, tonnage, and geological context.
    """
    deposits = []
    deposit_id = 1

    grade_categories = ["High (>44% Mn)", "Medium (35-44% Mn)", "Low (25-35% Mn)"]
    geological_types = [
        "Sedimentary (Gondite series)",
        "Metamorphic (Kodurite series)",
        "Lateritic (Supergene enrichment)",
        "Volcanogenic (Dharwar Supergroup)",
    ]
    status_options = ["Active Mining", "Exploration Phase", "Exhausted", "Under Assessment"]

    for state, info in MANGANESE_BELTS.items():
        lat_center, lon_center = info["center"]
        n_deposits = max(5, int(info["share_pct"] * 1.5))

        for _ in range(n_deposits):
            # Scatter deposits around belt center with realistic spread
            lat = lat_center + np.random.normal(0, 0.8)
            lon = lon_center + np.random.normal(0, 0.8)

            # Higher share states tend to have higher grade deposits
            grade_weights = (
                [0.4, 0.4, 0.2] if info["share_pct"] > 15
                else [0.2, 0.5, 0.3] if info["share_pct"] > 8
                else [0.1, 0.4, 0.5]
            )
            grade = np.random.choice(grade_categories, p=grade_weights)

            # Tonnage correlates with grade and state share
            base_tonnage = info["share_pct"] * np.random.uniform(0.5, 3.0)
            if "High" in grade:
                tonnage = base_tonnage * np.random.uniform(1.5, 4.0)
            elif "Medium" in grade:
                tonnage = base_tonnage * np.random.uniform(0.8, 2.5)
            else:
                tonnage = base_tonnage * np.random.uniform(0.3, 1.5)

            district = np.random.choice(info["districts"])
            geo_type = np.random.choice(geological_types)
            status = np.random.choice(
                status_options,
                p=[0.35, 0.30, 0.15, 0.20]
            )

            deposits.append({
                "deposit_id": f"MN-{deposit_id:04d}",
                "state": state,
                "district": district,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "grade": grade,
                "mn_pct": round(
                    np.random.uniform(44, 52) if "High" in grade
                    else np.random.uniform(35, 44) if "Medium" in grade
                    else np.random.uniform(25, 35),
                    1
                ),
                "estimated_tonnage_mt": round(tonnage, 2),
                "geological_type": geo_type,
                "depth_m": round(np.random.uniform(5, 150), 1),
                "status": status,
                "discovery_year": np.random.randint(1960, 2023),
            })
            deposit_id += 1

    df = pd.DataFrame(deposits)
    output_path = os.path.join(DATA_DIR, "manganese_deposits.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} deposit records → {output_path}")
    return df


def generate_prospectivity_grid():
    """
    Generate ~2000 grid cells covering India's manganese belts with
    spectral features and ML-derived prospectivity scores.
    """
    grid_cells = []
    cell_id = 1

    for state, info in MANGANESE_BELTS.items():
        lat_center, lon_center = info["center"]

        # Number of grid cells proportional to state's share
        n_cells = max(80, int(info["share_pct"] * 8))

        for _ in range(n_cells):
            lat = lat_center + np.random.uniform(-1.5, 1.5)
            lon = lon_center + np.random.uniform(-1.5, 1.5)

            # Distance from belt center affects prospectivity
            dist_from_center = np.sqrt(
                (lat - lat_center) ** 2 + (lon - lon_center) ** 2
            )

            # Simulate Sentinel-2 band reflectance values (0-1 range)
            b2 = np.random.uniform(0.02, 0.15)   # Blue
            b3 = np.random.uniform(0.03, 0.18)   # Green
            b4 = np.random.uniform(0.02, 0.20)   # Red
            b8 = np.random.uniform(0.10, 0.45)   # NIR
            b11 = np.random.uniform(0.08, 0.40)  # SWIR-1
            b12 = np.random.uniform(0.05, 0.35)  # SWIR-2

            # Compute spectral indices
            ndvi = (b8 - b4) / (b8 + b4 + 1e-10)
            clay_index = b11 / (b12 + 1e-10)
            ferrous_index = b11 / (b8 + 1e-10)
            mn_proxy = (b11 - b12) / (b11 + b12 + 1e-10)

            # Terrain features
            elevation = np.random.uniform(100, 1200)
            slope = np.random.uniform(0, 35)
            distance_to_fault = np.random.uniform(0, 50)

            # Prospectivity score: higher near belt centers with favorable spectral signatures
            # Simulates what a trained ML model would output
            base_score = max(0, 1.0 - dist_from_center / 2.0)
            spectral_bonus = (
                0.15 * (1 - ndvi) +          # Low vegetation → more mineral exposure
                0.10 * clay_index +            # Clay alteration
                0.20 * ferrous_index +         # Iron/Mn minerals
                0.15 * abs(mn_proxy) +         # Mn anomaly
                0.05 * (1 - slope / 35)        # Moderate terrain
            )
            fault_bonus = max(0, 0.15 * (1 - distance_to_fault / 50))

            raw_score = base_score * 0.5 + spectral_bonus + fault_bonus
            # Add noise and clamp
            prospectivity = np.clip(
                raw_score + np.random.normal(0, 0.08),
                0.0, 1.0
            )

            # Confidence based on data quality
            confidence = np.clip(
                0.5 + base_score * 0.3 + np.random.normal(0, 0.1),
                0.3, 0.99
            )

            # Classification
            if prospectivity >= 0.7:
                priority = "High"
            elif prospectivity >= 0.45:
                priority = "Medium"
            else:
                priority = "Low"

            grid_cells.append({
                "cell_id": f"CELL-{cell_id:05d}",
                "state": state,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "B2": round(b2, 4),
                "B3": round(b3, 4),
                "B4": round(b4, 4),
                "B8": round(b8, 4),
                "B11": round(b11, 4),
                "B12": round(b12, 4),
                "ndvi": round(ndvi, 4),
                "clay_index": round(clay_index, 4),
                "ferrous_index": round(ferrous_index, 4),
                "mn_proxy": round(mn_proxy, 4),
                "elevation": round(elevation, 1),
                "slope": round(slope, 1),
                "distance_to_fault": round(distance_to_fault, 1),
                "prospectivity_score": round(prospectivity, 4),
                "confidence": round(confidence, 4),
                "priority": priority,
            })
            cell_id += 1

    df = pd.DataFrame(grid_cells)
    output_path = os.path.join(DATA_DIR, "prospectivity_grid.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} grid cells → {output_path}")
    return df


def generate_production_data():
    """
    Generate 10 years of state-wise manganese production data
    with realistic patterns showing production shortfalls.
    """
    records = []

    # Base production by state (in '000 tonnes)
    state_base_production = {
        "Odisha": 1200,
        "Karnataka": 600,
        "Madhya Pradesh": 450,
        "Maharashtra": 400,
        "Goa": 250,
        "Andhra Pradesh": 180,
        "Rajasthan": 80,
        "Jharkhand": 70,
    }

    # Target is always higher than actual (showing shortfall)
    for year in PRODUCTION_YEARS:
        year_offset = year - 2014

        for state, base_prod in state_base_production.items():
            # Actual production with trend and noise
            trend = 1.0 + year_offset * np.random.uniform(-0.01, 0.03)
            seasonal = 1.0 + 0.05 * np.sin(2 * np.pi * year_offset / 4)
            noise = np.random.normal(1.0, 0.08)

            actual = base_prod * trend * seasonal * noise

            # Target production (always somewhat higher)
            target = base_prod * (1.0 + year_offset * 0.04) * np.random.uniform(1.1, 1.3)

            # Capacity utilization
            capacity = np.random.uniform(55, 85)

            # Number of active mines
            n_mines = max(3, int(base_prod / 50 + np.random.normal(0, 2)))

            shortfall = max(0, target - actual)
            shortfall_pct = (shortfall / target) * 100 if target > 0 else 0

            records.append({
                "year": year,
                "state": state,
                "actual_production_kt": round(actual, 1),
                "target_production_kt": round(target, 1),
                "shortfall_kt": round(shortfall, 1),
                "shortfall_pct": round(shortfall_pct, 1),
                "capacity_utilization_pct": round(capacity, 1),
                "active_mines": n_mines,
                "avg_grade_pct": round(np.random.uniform(30, 48), 1),
                "export_kt": round(actual * np.random.uniform(0.05, 0.20), 1),
                "domestic_consumption_kt": round(actual * np.random.uniform(0.70, 0.90), 1),
            })

    df = pd.DataFrame(records)
    output_path = os.path.join(DATA_DIR, "production_data.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} production records → {output_path}")
    return df


if __name__ == "__main__":
    print("=" * 60)
    print("  MANGANEX — Synthetic Data Generator")
    print("=" * 60)
    print()

    generate_deposit_data()
    generate_prospectivity_grid()
    generate_production_data()

    print()
    print("✅ All datasets generated successfully!")
    print(f"📂 Output directory: {DATA_DIR}")
