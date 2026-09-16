"""
MANGANEX — Prediction Module
Load trained model and score new grid cells for prospectivity.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml.feature_engineering import compute_all_features, get_feature_columns

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(PROJECT_ROOT, "ml", "models")


def load_model():
    """Load the trained prospectivity model and its metrics."""
    model_path = os.path.join(MODEL_DIR, "prospectivity_model.joblib")
    metrics_path = os.path.join(MODEL_DIR, "model_metrics.joblib")

    if not os.path.exists(model_path):
        return None, None

    model = joblib.load(model_path)
    metrics = joblib.load(metrics_path) if os.path.exists(metrics_path) else {}

    return model, metrics


def predict_prospectivity(model, df):
    """
    Score grid cells for manganese prospectivity.

    Args:
        model: Trained RandomForest model
        df: DataFrame with Sentinel-2 band values and terrain features

    Returns:
        DataFrame with added prediction columns
    """
    # Compute features
    df_features = compute_all_features(df)

    # Get feature columns used in training
    all_feature_cols = get_feature_columns()
    feature_cols = [c for c in all_feature_cols if c in df_features.columns]

    X = df_features[feature_cols].values

    # Predict
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    # Add to DataFrame
    result = df.copy()
    result["predicted_high"] = predictions
    result["prospectivity_probability"] = np.round(probabilities, 4)

    # Classify
    result["predicted_priority"] = pd.cut(
        probabilities,
        bins=[0, 0.3, 0.6, 1.0],
        labels=["Low", "Medium", "High"],
    )

    return result


def get_top_targets(df, n=20, min_score=0.5):
    """
    Extract top exploration targets from scored grid.

    Args:
        df: DataFrame with prospectivity scores
        n: Number of targets to return
        min_score: Minimum prospectivity score threshold

    Returns:
        DataFrame of top targets sorted by score
    """
    score_col = "prospectivity_score" if "prospectivity_score" in df.columns else "prospectivity_probability"

    filtered = df[df[score_col] >= min_score].copy()
    filtered = filtered.sort_values(score_col, ascending=False).head(n)
    filtered = filtered.reset_index(drop=True)
    filtered.index = filtered.index + 1  # 1-indexed ranking
    filtered.index.name = "rank"

    return filtered
