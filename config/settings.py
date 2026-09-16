"""
MineVision AI — Central Configuration
All app constants, color palettes, and geological parameters.
"""

# ─── App Metadata ────────────────────────────────────────────────────────
APP_TITLE = "MineVision AI"
APP_SUBTITLE = "Mn Reserve Intelligence"
APP_ICON = "💎"
VERSION = "1.0.0"
ORG_NAME = "MOIL LIMITED"
PROBLEM_STATEMENT = "SIH 2026 · Problem Statement: Mn Reserve Estimation"

# ─── Navigation Pages ────────────────────────────────────────────────────
PAGES = {
    "Command Center": "📊",
    "Prospectivity Map": "🗺️",
    "Production Forecast": "📈",
    "Risk Analysis": "⚠️",
    "Recommendations": "💡",
}

# ─── Map Configuration ──────────────────────────────────────────────────
MAP_CENTER = [21.5, 79.5]  # Central India / MOIL belt
MAP_ZOOM = 8
MAP_TILES = "OpenStreetMap"

# ─── Color Palette (Earth/Military Tones) ────────────────────────────────
COLORS = {
    "bg_main": "#141410",          # Main background
    "bg_sidebar": "#1a1a14",       # Sidebar background
    "bg_card": "#1e1e16",          # Card background
    "bg_card_alt": "#252518",      # Alternate card background
    "bg_surface": "#2a2a1e",       # Surface elements
    "border": "#3a3a2a",           # Card borders
    "border_light": "#4a4a3a",     # Lighter borders

    "accent": "#c8842a",           # Primary accent (warm amber/orange)
    "primary": "#c8842a",          # Alias for accent
    "accent_hover": "#d4943a",     # Accent hover
    "accent_dim": "rgba(200,132,42,0.15)",  # Accent dim background

    "success": "#5a8a3a",          # Active/success green
    "success_dim": "rgba(90,138,58,0.15)",

    "critical": "#c94a2a",         # Critical red-orange
    "high": "#c8842a",             # High risk (amber)
    "moderate": "#8a8a2a",         # Moderate (yellow-olive)
    "low": "#3a8a3a",              # Low risk (green)

    "text": "#e0ddd0",             # Primary text (warm cream)
    "text_secondary": "#8a8a7a",   # Secondary text
    "text_muted": "#5a5a4a",       # Muted text
    "text_header": "#b0ad9e",      # Header text

    "maintenance": "#c9a02a",      # Maintenance status yellow
    "idle": "#5a5a4a",             # Idle status gray
}

# Prospectivity colors
PROSPECTIVITY = {
    "high": "#c8842a",       # Orange — >75%
    "moderate": "#4aada8",   # Teal — 50-75%
    "low": "#8a8a7a",        # Gray — <50%
    "drill_hole": "#2a2a1e", # Dark — drill hole
}

# Chart color sequence
CHART_COLORS = [
    "#c8842a", "#4aada8", "#5a8a3a", "#c94a2a",
    "#8a8a2a", "#7a6a4a", "#a0785a", "#6a9a7a",
]

# ─── Sentinel-2 Band Definitions ────────────────────────────────────────
SENTINEL2_BANDS = {
    "B2": {"name": "Blue", "wavelength": "490nm", "resolution": 10},
    "B3": {"name": "Green", "wavelength": "560nm", "resolution": 10},
    "B4": {"name": "Red", "wavelength": "665nm", "resolution": 10},
    "B8": {"name": "NIR", "wavelength": "842nm", "resolution": 10},
    "B11": {"name": "SWIR-1", "wavelength": "1610nm", "resolution": 20},
    "B12": {"name": "SWIR-2", "wavelength": "2190nm", "resolution": 20},
}

# ─── Spectral Index Definitions ─────────────────────────────────────────
SPECTRAL_INDICES = {
    "NDVI": {
        "formula": "(B8 - B4) / (B8 + B4)",
        "description": "Normalized Difference Vegetation Index",
        "interpretation": "Low NDVI → barren/mineral-rich terrain",
    },
    "Clay Index": {
        "formula": "B11 / B12",
        "description": "Clay Mineral Ratio",
        "interpretation": "High values → clay-rich alteration zones",
    },
    "Ferrous Index": {
        "formula": "B11 / B8",
        "description": "Ferrous Minerals Index",
        "interpretation": "High values → iron/manganese-bearing minerals",
    },
    "Mn Proxy": {
        "formula": "(B11 - B12) / (B11 + B12)",
        "description": "Manganese Proxy Index",
        "interpretation": "Anomalous values → potential Mn enrichment",
    },
}

# ─── ML Configuration ───────────────────────────────────────────────────
ML_FEATURES = [
    "ndvi", "clay_index", "ferrous_index", "mn_proxy",
    "elevation", "slope", "distance_to_fault",
    "B2", "B3", "B4", "B8", "B11", "B12",
]

MODEL_PARAMS = {
    "n_estimators": 200,
    "max_depth": 12,
    "min_samples_split": 5,
    "min_samples_leaf": 3,
    "random_state": 42,
    "n_jobs": -1,
}

# ─── MOIL Mine Blocks ───────────────────────────────────────────────────
MINE_BLOCKS = [
    {"name": "Balaghat Mine", "state": "Madhya Pradesh", "lat": 21.81, "lon": 80.19, "status": "ACTIVE", "capacity_kt": 450, "grade_pct": 46},
    {"name": "Ukwa Mine", "state": "Madhya Pradesh", "lat": 21.75, "lon": 80.45, "status": "ACTIVE", "capacity_kt": 180, "grade_pct": 42},
    {"name": "Dongri Buzurg Mine", "state": "Maharashtra", "lat": 21.68, "lon": 79.88, "status": "ACTIVE", "capacity_kt": 320, "grade_pct": 44},
    {"name": "Gumgaon Mine", "state": "Maharashtra", "lat": 21.15, "lon": 79.10, "status": "MAINTENANCE", "capacity_kt": 220, "grade_pct": 38},
    {"name": "Kandri Mine", "state": "Maharashtra", "lat": 21.45, "lon": 79.13, "status": "ACTIVE", "capacity_kt": 150, "grade_pct": 40},
    {"name": "Munsar Mine", "state": "Maharashtra", "lat": 21.25, "lon": 79.55, "status": "IDLE", "capacity_kt": 90, "grade_pct": 35},
    {"name": "Tirodi Mine", "state": "Madhya Pradesh", "lat": 21.95, "lon": 79.72, "status": "ACTIVE", "capacity_kt": 130, "grade_pct": 41},
    {"name": "Chikla Mine", "state": "Maharashtra", "lat": 21.50, "lon": 78.90, "status": "ACTIVE", "capacity_kt": 110, "grade_pct": 39},
]

# ─── Indian Manganese Belts ─────────────────────────────────────────────
MANGANESE_BELTS = {
    "Odisha": {
        "center": [21.5, 84.5],
        "districts": ["Sundargarh", "Keonjhar", "Kalahandi", "Koraput", "Jajpur"],
        "share_pct": 34,
        "color": "#c8842a",
    },
    "Karnataka": {
        "center": [14.5, 75.5],
        "districts": ["Uttara Kannada", "Bellary", "Shimoga", "Chitradurga", "Tumkur"],
        "share_pct": 24,
        "color": "#4aada8",
    },
    "Madhya Pradesh": {
        "center": [22.5, 80.0],
        "districts": ["Balaghat", "Chhindwara", "Jhabua"],
        "share_pct": 12,
        "color": "#5a8a3a",
    },
    "Maharashtra": {
        "center": [21.0, 79.5],
        "districts": ["Nagpur", "Bhandara", "Ratnagiri"],
        "share_pct": 12,
        "color": "#c94a2a",
    },
    "Goa": {
        "center": [15.4, 74.0],
        "districts": ["North Goa", "South Goa"],
        "share_pct": 7,
        "color": "#8a8a2a",
    },
    "Andhra Pradesh": {
        "center": [18.5, 83.5],
        "districts": ["Srikakulam", "Vizianagaram", "Visakhapatnam"],
        "share_pct": 5,
        "color": "#7a6a4a",
    },
    "Rajasthan": {
        "center": [25.5, 73.5],
        "districts": ["Banswara", "Udaipur"],
        "share_pct": 3,
        "color": "#a0785a",
    },
    "Jharkhand": {
        "center": [22.8, 85.5],
        "districts": ["West Singhbhum", "East Singhbhum"],
        "share_pct": 3,
        "color": "#6a9a7a",
    },
}

# ─── Production Data Constants ───────────────────────────────────────────
PRODUCTION_YEARS = list(range(2014, 2025))
INDIA_MN_TARGET_MT = 4.5
INDIA_MN_ACTUAL_AVG_MT = 3.2
