# ============================================================
# MachineGuardAI - Local Model Training Script
# Trains a Random Forest Classifier on the cleaned dataset
# and saves the model + preprocessor to models/
# ============================================================
#
# Usage:
#   python train_local_model.py
#
# Output:
#   models/predictive_model.joblib  - trained RandomForestClassifier
#   models/label_encoder.joblib     - LabelEncoder fitted on Product ID prefix
# ============================================================

import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ── Paths ────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "data", "predictive_maintenance_clean_shaped.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "predictive_model.joblib")
ENC_PATH   = os.path.join(MODELS_DIR, "label_encoder.joblib")

os.makedirs(MODELS_DIR, exist_ok=True)

# ── 1. Load Dataset ──────────────────────────────────────────
print("Loading dataset ...")
df = pd.read_csv(DATA_PATH)
print(f"  Rows: {len(df):,}  |  Columns: {list(df.columns)}")

# ── 2. Feature Engineering ───────────────────────────────────
# The Product ID prefix (L / M / H) encodes quality tier and
# is a meaningful predictor. Extract it as a numeric-encoded
# column; save the encoder so prediction time uses the same mapping.
df["Product_Prefix"] = df["Product ID"].str[0]

le = LabelEncoder()
df["Product_Prefix_Enc"] = le.fit_transform(df["Product_Prefix"])

FEATURE_COLS = [
    "Product_Prefix_Enc",       # encoded quality tier (L/M/H)
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]
TARGET_COL = "Failure Type"

X = df[FEATURE_COLS].astype(float)
y = df[TARGET_COL]

print(f"\nClass distribution:\n{y.value_counts().to_string()}")

# ── 3. Train / Test Split ────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y,          # preserve class proportions in both splits
)
print(f"\nTrain size: {len(X_train):,}  |  Test size: {len(X_test):,}")

# ── 4. Train Random Forest ───────────────────────────────────
print("\nTraining Random Forest ...")
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,         # grow full trees - dataset is small enough
    min_samples_split=4,
    class_weight="balanced",  # handle the heavy No Failure majority
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)
print("  Training complete.")

# ── 5. Evaluate ──────────────────────────────────────────────
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n{'='*55}")
print(f"  Accuracy : {accuracy * 100:.2f} %")
print(f"{'='*55}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
# Pretty-print with class labels
cm_df = pd.DataFrame(cm, index=model.classes_, columns=model.classes_)
print(cm_df.to_string())

# ── 6. Verify predict_proba is available ─────────────────────
assert hasattr(model, "predict_proba"), (
    "RandomForestClassifier must support predict_proba(). "
    "This should never fail — check scikit-learn installation."
)
print("\n  predict_proba() confirmed available for confidence scores.")

# ── 7. Save Artefacts ────────────────────────────────────────
joblib.dump(model, MODEL_PATH)
joblib.dump(le,    ENC_PATH)

print(f"\nSaved model   : {MODEL_PATH}")
print(f"Saved encoder : {ENC_PATH}")
print("\nDone. Run your Streamlit app to use local inference.")
