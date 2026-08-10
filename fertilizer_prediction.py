# ============================================================
# Fertilizer Prediction — ML Project
# ============================================================
# Predict the best fertilizer based on soil, crop & climate.
# Models: Random Forest, Decision Tree, KNN
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# --------------------------------------------------
# Configuration
# --------------------------------------------------
DATA_PATH = os.path.join("data", "Fertilizer_Prediction.csv")
CHART_DIR = "output_charts_fertilizer"
os.makedirs(CHART_DIR, exist_ok=True)

# Plot style
sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams.update({"figure.dpi": 120, "savefig.bbox": "tight"})


# ==================================================
# 1. LOAD & EXPLORE DATA
# ==================================================
print("=" * 60)
print("1. LOADING DATA")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

print(f"\nShape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nBasic statistics:\n{df.describe()}")

# Identify the target column
target_col = "Fertilizer Name"
print(f"\nTarget classes ({df[target_col].nunique()}): {sorted(df[target_col].unique())}")


# ==================================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# ==================================================
print("\n" + "=" * 60)
print("2. EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# --- 2a. Class distribution ---
fig, ax = plt.subplots(figsize=(12, 6))
class_counts = df[target_col].value_counts().sort_index()
class_counts.plot(kind="bar", color=sns.color_palette("viridis", len(class_counts)), ax=ax)
ax.set_title("Fertilizer Class Distribution", fontsize=16, fontweight="bold")
ax.set_xlabel("Fertilizer", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "01_class_distribution.png"))
plt.close()
print("  [OK] Saved: 01_class_distribution.png")

# --- 2b. Soil Type distribution ---
fig, ax = plt.subplots(figsize=(10, 5))
df["Soil Type"].value_counts().plot(kind="bar", color=sns.color_palette("mako", df["Soil Type"].nunique()), ax=ax)
ax.set_title("Soil Type Distribution", fontsize=14, fontweight="bold")
ax.set_xlabel("Soil Type", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "02_soil_type_distribution.png"))
plt.close()
print("  [OK] Saved: 02_soil_type_distribution.png")

# --- 2c. Crop Type distribution ---
fig, ax = plt.subplots(figsize=(10, 5))
df["Crop Type"].value_counts().plot(kind="bar", color=sns.color_palette("rocket", df["Crop Type"].nunique()), ax=ax)
ax.set_title("Crop Type Distribution", fontsize=14, fontweight="bold")
ax.set_xlabel("Crop Type", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "03_crop_type_distribution.png"))
plt.close()
print("  [OK] Saved: 03_crop_type_distribution.png")

# --- 2d. Numeric feature distributions ---
numeric_features = ["Temperature", "Humidity", "Moisture", "Nitrogen", "Phosphorous", "Potassium"]
fig, axes = plt.subplots(2, 3, figsize=(16, 8))
axes = axes.flatten()
for i, col in enumerate(numeric_features):
    if col in df.columns:
        sns.histplot(df[col], kde=True, ax=axes[i], color=sns.color_palette("viridis")[i % 6])
        axes[i].set_title(col, fontsize=12, fontweight="bold")
fig.suptitle("Numeric Feature Distributions", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "04_feature_distributions.png"))
plt.close()
print("  [OK] Saved: 04_feature_distributions.png")

# --- 2e. Correlation heatmap (numeric only) ---
fig, ax = plt.subplots(figsize=(10, 8))
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True,
            linewidths=0.5, ax=ax)
ax.set_title("Feature Correlation Heatmap", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "05_correlation_heatmap.png"))
plt.close()
print("  [OK] Saved: 05_correlation_heatmap.png")


# ==================================================
# 3. PREPROCESSING
# ==================================================
print("\n" + "=" * 60)
print("3. PREPROCESSING")
print("=" * 60)

# Label-encode categorical columns
le_soil = LabelEncoder()
le_crop = LabelEncoder()

df["Soil Type_encoded"] = le_soil.fit_transform(df["Soil Type"])
df["Crop Type_encoded"] = le_crop.fit_transform(df["Crop Type"])

print(f"  Soil Type mapping: {dict(zip(le_soil.classes_, le_soil.transform(le_soil.classes_)))}")
print(f"  Crop Type mapping: {dict(zip(le_crop.classes_, le_crop.transform(le_crop.classes_)))}")

# Define features (use encoded categorical + numeric)
feature_cols = ["Temperature", "Humidity", "Moisture", "Soil Type_encoded",
                "Crop Type_encoded", "Nitrogen", "Phosphorous", "Potassium"]

# Filter to only existing columns
feature_cols = [c for c in feature_cols if c in df.columns]

X = df[feature_cols]
y = df[target_col]

# Train/Test split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\n  Train set: {X_train.shape[0]} samples")
print(f"  Test set:  {X_test.shape[0]} samples")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("  [OK] Features scaled with StandardScaler")


# ==================================================
# 4. TRAIN MODELS
# ==================================================
print("\n" + "=" * 60)
print("4. TRAINING MODELS")
print("=" * 60)

models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5),
}

results = {}

for name, model in models.items():
    print(f"\n  Training: {name}...")
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    results[name] = {"model": model, "predictions": y_pred, "accuracy": acc}
    print(f"  [OK] {name} - Accuracy: {acc:.4f} ({acc*100:.2f}%)")


# ==================================================
# 5. EVALUATION
# ==================================================
print("\n" + "=" * 60)
print("5. EVALUATION")
print("=" * 60)

for name, res in results.items():
    print(f"\n{'-' * 50}")
    print(f"  {name} - Accuracy: {res['accuracy']:.4f}")
    print(f"{'-' * 50}")
    print(classification_report(y_test, res["predictions"], zero_division=0))

    # Confusion matrix heatmap
    labels = sorted(y.unique())
    cm = confusion_matrix(y_test, res["predictions"], labels=labels)
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_title(f"Confusion Matrix - {name}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Predicted", fontsize=12)
    ax.set_ylabel("Actual", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    fname = f"06_confusion_matrix_{name.lower().replace(' ', '_')}.png"
    plt.savefig(os.path.join(CHART_DIR, fname))
    plt.close()
    print(f"  [OK] Saved: {fname}")

# --- Accuracy comparison bar chart ---
fig, ax = plt.subplots(figsize=(8, 5))
model_names = list(results.keys())
accuracies = [results[n]["accuracy"] for n in model_names]
colors = sns.color_palette("viridis", len(model_names))
bars = ax.bar(model_names, accuracies, color=colors, edgecolor="black", linewidth=0.5)
for bar, acc in zip(bars, accuracies):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f"{acc:.2%}", ha="center", fontsize=12, fontweight="bold")
ax.set_title("Model Accuracy Comparison", fontsize=16, fontweight="bold")
ax.set_ylabel("Accuracy", fontsize=12)
ax.set_ylim(0, 1.1)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "07_accuracy_comparison.png"))
plt.close()
print("\n  [OK] Saved: 07_accuracy_comparison.png")

# --- Feature importance (Random Forest) ---
rf_model = results["Random Forest"]["model"]
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(range(len(feature_cols)), importances[indices],
       color=sns.color_palette("viridis", len(feature_cols)))
ax.set_xticks(range(len(feature_cols)))
ax.set_xticklabels([feature_cols[i] for i in indices], rotation=45, ha="right")
ax.set_title("Feature Importance (Random Forest)", fontsize=16, fontweight="bold")
ax.set_ylabel("Importance", fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "08_feature_importance.png"))
plt.close()
print("  [OK] Saved: 08_feature_importance.png")


# ==================================================
# 6. SUMMARY
# ==================================================
print("\n" + "=" * 60)
print("6. SUMMARY")
print("=" * 60)
print(f"\n  {'Model':<20} {'Accuracy':>10}")
print(f"  {'-' * 32}")
for name, res in results.items():
    print(f"  {name:<20} {res['accuracy']:>10.4f}")

best_model = max(results, key=lambda k: results[k]["accuracy"])
print(f"\n  [*] Best Model: {best_model} ({results[best_model]['accuracy']:.2%})")
print(f"\n  All charts saved to: {CHART_DIR}/")
print("=" * 60)
