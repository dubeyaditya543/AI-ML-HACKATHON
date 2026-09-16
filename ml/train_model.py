"""
MANGANEX — Model Training Pipeline
Random Forest classifier with spatial cross-validation for manganese prospectivity mapping.

Usage:
    python ml/train_model.py
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, cross_val_score
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    classification_report, confusion_matrix
)
from sklearn.preprocessing import LabelEncoder

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import MODEL_PARAMS
from ml.feature_engineering import compute_all_features, get_feature_columns

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODEL_DIR = os.path.join(PROJECT_ROOT, "ml", "models")


def load_training_data():
    """Load and prepare training data from the prospectivity grid."""
    grid_path = os.path.join(DATA_DIR, "prospectivity_grid.csv")

    if not os.path.exists(grid_path):
        print("❌ prospectivity_grid.csv not found. Run generate_synthetic_data.py first.")
        sys.exit(1)

    df = pd.read_csv(grid_path)
    print(f"📊 Loaded {len(df)} grid cells from {grid_path}")
    return df


def prepare_features_and_labels(df):
    """
    Prepare feature matrix X and label vector y.
    Labels are derived from the prospectivity priority classification.
    """
    # Recompute spectral features to ensure consistency
    df = compute_all_features(df)

    # Get feature columns that exist in the data
    all_feature_cols = get_feature_columns()
    feature_cols = [c for c in all_feature_cols if c in df.columns]

    X = df[feature_cols].values
    
    # Binary classification: High priority vs. not
    y = (df["priority"] == "High").astype(int).values

    # Groups for spatial CV (by state to prevent spatial leakage)
    groups = LabelEncoder().fit_transform(df["state"].values)

    print(f"📐 Feature matrix: {X.shape}")
    print(f"🎯 Class distribution: {np.bincount(y)} (0=Non-High, 1=High)")

    return X, y, groups, feature_cols


def train_model(X, y, groups, feature_cols):
    """
    Train a Random Forest classifier with spatial cross-validation.
    """
    print("\n🔧 Training Random Forest Classifier...")
    print(f"   Parameters: {MODEL_PARAMS}")

    # Initialize model
    model = RandomForestClassifier(**MODEL_PARAMS)

    # Spatial cross-validation using GroupKFold
    n_splits = min(5, len(np.unique(groups)))
    gkf = GroupKFold(n_splits=n_splits)

    print(f"\n📊 Spatial Cross-Validation ({n_splits}-fold by state):")

    cv_scores = {
        "accuracy": [],
        "f1": [],
    }

    for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups), 1):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        model_fold = RandomForestClassifier(**MODEL_PARAMS)
        model_fold.fit(X_train, y_train)
        y_pred = model_fold.predict(X_val)

        acc = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred, zero_division=0)

        cv_scores["accuracy"].append(acc)
        cv_scores["f1"].append(f1)

        print(f"   Fold {fold}: Accuracy={acc:.4f}, F1={f1:.4f}")

    print(f"\n   Mean Accuracy: {np.mean(cv_scores['accuracy']):.4f} ± {np.std(cv_scores['accuracy']):.4f}")
    print(f"   Mean F1 Score: {np.mean(cv_scores['f1']):.4f} ± {np.std(cv_scores['f1']):.4f}")

    # Train final model on all data
    print("\n🏋️ Training final model on all data...")
    model.fit(X, y)

    # Feature importance
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]

    print("\n📊 Feature Importance (Top 10):")
    for i in range(min(10, len(feature_cols))):
        idx = sorted_idx[i]
        print(f"   {i+1}. {feature_cols[idx]}: {importances[idx]:.4f}")

    # Final metrics on training data (for reference)
    y_pred_final = model.predict(X)
    y_prob_final = model.predict_proba(X)[:, 1]

    print(f"\n📈 Final Model Metrics (on full training set):")
    print(f"   Accuracy: {accuracy_score(y, y_pred_final):.4f}")
    print(f"   F1 Score: {f1_score(y, y_pred_final):.4f}")
    print(f"   ROC-AUC:  {roc_auc_score(y, y_prob_final):.4f}")

    return model, {
        "feature_names": feature_cols,
        "feature_importances": dict(zip(feature_cols, importances.tolist())),
        "cv_accuracy_mean": float(np.mean(cv_scores["accuracy"])),
        "cv_accuracy_std": float(np.std(cv_scores["accuracy"])),
        "cv_f1_mean": float(np.mean(cv_scores["f1"])),
        "cv_f1_std": float(np.std(cv_scores["f1"])),
        "train_accuracy": float(accuracy_score(y, y_pred_final)),
        "train_f1": float(f1_score(y, y_pred_final)),
        "train_roc_auc": float(roc_auc_score(y, y_prob_final)),
        "n_samples": int(len(y)),
        "n_features": int(X.shape[1]),
        "class_distribution": {"non_high": int(np.sum(y == 0)), "high": int(np.sum(y == 1))},
    }


def save_model(model, metrics, feature_cols):
    """Save trained model and metadata."""
    os.makedirs(MODEL_DIR, exist_ok=True)

    model_path = os.path.join(MODEL_DIR, "prospectivity_model.joblib")
    joblib.dump(model, model_path)
    print(f"\n💾 Model saved → {model_path}")

    # Save metrics
    metrics_path = os.path.join(MODEL_DIR, "model_metrics.joblib")
    joblib.dump(metrics, metrics_path)
    print(f"💾 Metrics saved → {metrics_path}")

    return model_path


if __name__ == "__main__":
    print("=" * 60)
    print("  MANGANEX — Model Training Pipeline")
    print("=" * 60)
    print()

    # Load data
    df = load_training_data()

    # Prepare features
    X, y, groups, feature_cols = prepare_features_and_labels(df)

    # Train model
    model, metrics = train_model(X, y, groups, feature_cols)

    # Save
    save_model(model, metrics, feature_cols)

    print("\n✅ Training pipeline complete!")
