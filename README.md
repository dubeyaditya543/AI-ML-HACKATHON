<<<<<<< HEAD
# AI-ML-HACKATHON
#akshat
=======
# 💎 MineVision AI — Manganese Reserve Intelligence & Production Planning

> **Smart India Hackathon 2026**  
> **Problem Statement:** *Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls*  
> **Operating Entity Context:** *MOIL Limited & Ministry of Mines, Government of India*

---

## 🌟 Executive Summary

**MineVision AI** is an enterprise-grade exploration and production intelligence platform designed to assist mining geologists, planning engineers, and executives in:
1. **Discovering Blind Manganese Deposits:** Integrating multi-spectral satellite imagery (Sentinel-2) with machine learning to identify hidden reserves in India's major manganese belts (Central Belt: Nagpur-Bhandara-Balaghat, Odisha, Karnataka).
2. **Eliminating Production Shortfalls:** Tracking mine-level downtime and bottlenecks (e.g. Gumgaon dewatering, Balaghat hoisting limits) and simulating what-if operational levers (mechanization, new blocks, beneficiation) to bridge the national demand gap.

---

## 📁 Repository Directory Breakdown

Below is a detailed walkthrough of every folder in the codebase, explaining what is happening inside it and what it does:

```
SIH/
├── .streamlit/                     # Streamlit theme & server configuration
├── config/                         # App-wide constants, color themes, mine metadata
├── data/                           # Datasets & synthetic data generator
├── ml/                             # ML training, feature engineering & inference
├── gee/                            # Google Earth Engine Sentinel-2 satellite connector
├── components/                     # Modular UI page views & dashboards
├── utils/                          # Geospatial & Plotly chart helper utilities
├── app.py                          # Streamlit application entry point & router
└── requirements.txt                # Python environment dependencies
```

---

### 1. `config/` — System Configuration & Constants
The `config/` folder acts as the single source of truth for all parameters across the frontend, data layer, and ML models.

- **[`config/settings.py`](file:///d:/COLLEGE/PROJECTS/SIH/config/settings.py)**:
  - **Color Palette (`COLORS`)**: Defines the dark olive/earth tone UI theme (`#141410` background, `#1a1a14` sidebar, `#1e1e16` cards, `#c8842a` warm amber accent, `#5c9e47` green, `#c94a2a` red).
  - **MOIL Mine Blocks (`MINE_BLOCKS`)**: Geo-coordinates, operational statuses (ACTIVE, MAINTENANCE, IDLE), annual capacities (kt), and ore grades (% Mn) for key mines: Balaghat, Ukwa, Dongri Buzurg, Gumgaon, Kandri, Munsar, Tirodi, and Chikla.
  - **Manganese Belt Definitions (`MANGANESE_BELTS`)**: Geographic bounding boxes and national reserve share percentages for Odisha (34%), Karnataka (24%), Madhya Pradesh (12%), Maharashtra (12%), and others.
  - **Satellite & Indices Metadata**: Specifications for Sentinel-2 spectral bands (B2, B3, B4, B8, B11, B12) and mathematical formulas for geological indices (NDVI, Clay Index, Ferrous Index, Mn Proxy).
  - **ML Configuration**: Feature column lists and Random Forest hyperparameter dictionaries.

---

### 2. `data/` — Geospatial & Production Datasets
The `data/` folder stores the operational, spatial, and geological datasets used throughout the app.

- **[`data/generate_synthetic_data.py`](file:///d:/COLLEGE/PROJECTS/SIH/data/generate_synthetic_data.py)**:
  - A deterministic simulation script based on published geological parameters from the Geological Survey of India (GSI) and Indian Bureau of Mines (IBM).
  - Generates realistic datasets when direct proprietary GIS drill-hole feeds are offline.
- **[`data/manganese_deposits.csv`](file:///d:/COLLEGE/PROJECTS/SIH/data/manganese_deposits.csv)**:
  - 150+ deposit records across Indian mining districts with latitude, longitude, grade class, estimated tonnage (Mt), host rock type (Gondite, Kodurite, Dharwar, Lateritic), depth, and exploration status.
- **[`data/prospectivity_grid.csv`](file:///d:/COLLEGE/PROJECTS/SIH/data/prospectivity_grid.csv)**:
  - High-density 50m resolution exploration grid containing surface spectral values (B2-B12 reflectances), computed indices (NDVI, Clay, Ferrous, Mn Proxy), digital elevation model (DEM) metrics (slope, elevation), fault proximity, and AI-predicted prospectivity scores (0.0 to 1.0).
- **[`data/production_data.csv`](file:///d:/COLLEGE/PROJECTS/SIH/data/production_data.csv)**:
  - 10-year historical and planned production data (2014–2024), tracking national targets (4.9 Mt), actual outputs, state-by-state breakdowns, and annual shortfall volumes.

---

### 3. `ml/` — Machine Learning Pipeline
The `ml/` folder houses the intelligence engine that predicts manganese mineralization probability from satellite and geophysical indicators.

- **[`ml/feature_engineering.py`](file:///d:/COLLEGE/PROJECTS/SIH/ml/feature_engineering.py)**:
  - Computes band ratio proxies:
    - **NDVI** = `(B8 - B4) / (B8 + B4)` (Vegetation masking)
    - **Clay Index** = `B11 / B12` (Hydrothermal alteration zones)
    - **Ferrous Index** = `B11 / B8` (Iron & manganese association)
    - **Mn Proxy** = `(B11 - B12) / (B11 + B12)` (SWIR spectral absorption anomaly)
  - Prepares spatial feature matrices incorporating terrain elevation and fault line distances.
- **[`ml/train_model.py`](file:///d:/COLLEGE/PROJECTS/SIH/ml/train_model.py)**:
  - Trains a `RandomForestClassifier` with spatial cross-validation (`GroupKFold` grouped by geographical region to prevent spatial autocorrelation leakage between training and testing sets).
  - Evaluates ROC-AUC (~99.8%), precision, recall, and feature importances.
  - Serializes model weights to `ml/models/manganese_rf_model.pkl`.
- **[`ml/predict.py`](file:///d:/COLLEGE/PROJECTS/SIH/ml/predict.py)**:
  - Inference utility to load the serialized model, score unseen coordinates, and classify targets into High (>75%), Moderate (50-75%), or Low (<50%) exploration priorities.

---

### 4. `gee/` — Earth Engine Satellite Integration
The `gee/` folder connects the system to live satellite imagery providers.

- **[`gee/sentinel_fetcher.py`](file:///d:/COLLEGE/PROJECTS/SIH/gee/sentinel_fetcher.py)**:
  - Google Earth Engine (GEE) Python API connector for the `COPERNICUS/S2_SR_HARMONIZED` collection (Sentinel-2 Level-2A surface reflectance).
  - Performs QA60 band cloud masking, median seasonal composite generation, and bounding-box image extraction.
  - Provides graceful fallbacks to cached synthetic spectral grids if GEE cloud authentication is not initialized.

---

### 5. `components/` — UI Views & Command Center Dashboards
The `components/` folder holds the modular UI views that render the 5 core navigation screens of the MineVision AI platform.

- **[`components/sidebar.py`](file:///d:/COLLEGE/PROJECTS/SIH/components/sidebar.py)**:
  - Renders the custom navigation sidebar featuring the `● MineVision AI` brand, navigation pills, and `MOIL LIMITED / MN RESERVE INTELLIGENCE` technical footer.
- **[`components/command_center.py`](file:///d:/COLLEGE/PROJECTS/SIH/components/command_center.py)**:
  - **Executive Command Center (Screen 1)**:
    - 5 KPI metric cards: Predicted Production (4,210 t ↘), Target (4,900 t), Shortfall Risk (34% ⚠️), Recoverable Production (3,200 t), High Prospectivity Areas (9).
    - **Mine Block Status**: Real-time status list of Balaghat, Ukwa, Dongri Buzurg, Gumgaon, Kandri, Munsar.
    - **Highest Shortfall Risk**: Ranked vulnerability list with Critical, High, Moderate, and Low status pills.
- **[`components/prospectivity_map.py`](file:///d:/COLLEGE/PROJECTS/SIH/components/prospectivity_map.py)**:
  - **AI Prospectivity Map (Screen 2)**:
    - Interactive satellite basemap centered on the Nagpur-Balaghat MOIL belt.
    - Color-coded prospectivity hotspots (Orange = >75%, Teal = 50-75%, Slate = <50%) and white drill-hole indicators.
    - Right-hand control panel with Legend, interactive **Cell Inspector** (showing lat/long, AI score, grade %, and Sentinel-2 index values), and Data Category disclosures.
- **[`components/production_forecast.py`](file:///d:/COLLEGE/PROJECTS/SIH/components/production_forecast.py)**:
  - **Production Forecast (Screen 3)**:
    - Multi-year trajectory comparing historical production, baseline AI forecasts, and national demand targets.
    - Interactive what-if scenario sliders (underground mechanization, fast-tracked exploration blocks, beneficiation yield) that instantly compute recovered tonnage and target gap closure.
- **[`components/risk_analysis.py`](file:///d:/COLLEGE/PROJECTS/SIH/components/risk_analysis.py)**:
  - **Risk Analysis (Screen 4)**:
    - Fleet risk matrix plotting downtime probability against tonnage impact.
    - Ore grade dilution curves and mine-by-mine vulnerability register.
- **[`components/recommendations.py`](file:///d:/COLLEGE/PROJECTS/SIH/components/recommendations.py)**:
  - **Strategic Recommendations (Screen 5)**:
    - Ranked AI exploration drill targets with GPS coordinates, predicted grades, and priority ratings.
    - Operational intervention action items (Gumgaon dewatering, Balaghat skip hoist upgrade, DMS beneficiation).

---

### 6. `utils/` — Helper Utilities
The `utils/` folder provides common geospatial, computational, and charting utilities.

- **[`utils/geo_utils.py`](file:///d:/COLLEGE/PROJECTS/SIH/utils/geo_utils.py)**:
  - Haversine great-circle distance formulas, bounding-box calculators, regular coordinate grid generators, and GeoJSON point converters.
- **[`utils/chart_utils.py`](file:///d:/COLLEGE/PROJECTS/SIH/utils/chart_utils.py)**:
  - Reusable Plotly chart builders styled for the dark olive theme (bar charts, area charts, donut charts, gauge meters, radar diagrams).

---

### 7. `.streamlit/` — Streamlit Runtime Configuration
- **[` .streamlit/config.toml`](file:///d:/COLLEGE/PROJECTS/SIH/.streamlit/config.toml)**:
  - Sets the base theme tokens (`backgroundColor = "#141410"`, `secondaryBackgroundColor = "#1a1a14"`, `primaryColor = "#c8842a"`, `textColor = "#e0ddd0"`, `font = "monospace"`).
  - Configures headless execution on port `8501`.

---

## 🚀 How to Run

1. **Activate your environment & install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Generate data & train model:**
   ```bash
   python data/generate_synthetic_data.py
   python ml/train_model.py
   ```
3. **Launch the MineVision AI dashboard:**
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.
>>>>>>> origin/ML-Integration
