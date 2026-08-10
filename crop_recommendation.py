# ============================================================
# Crop Recommendation — ML Project
# ============================================================
# Predict the best crop to grow based on soil & climate data.
# Models: Random Forest, Decision Tree, KNN
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
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
DATA_PATH = os.path.join("data", "Crop_recommendation.csv")
CHART_DIR = "output_charts"
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
print(f"\nTarget classes ({df['label'].nunique()}): {sorted(df['label'].unique())}")


# ==================================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# ==================================================
print("\n" + "=" * 60)
print("2. EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# --- 2a. Class distribution ---
fig, ax = plt.subplots(figsize=(14, 6))
df["label"].value_counts().sort_index().plot(kind="bar", color=sns.color_palette("viridis", df["label"].nunique()), ax=ax)
ax.set_title("Crop Class Distribution", fontsize=16, fontweight="bold")
ax.set_xlabel("Crop", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "01_class_distribution.png"))
plt.close()
print("  [OK] Saved: 01_class_distribution.png")

# --- 2b. Correlation heatmap ---
fig, ax = plt.subplots(figsize=(10, 8))
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True,
            linewidths=0.5, ax=ax)
ax.set_title("Feature Correlation Heatmap", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "02_correlation_heatmap.png"))
plt.close()
print("  [OK] Saved: 02_correlation_heatmap.png")

# --- 2c. Feature distributions ---
features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
fig, axes = plt.subplots(2, 4, figsize=(18, 8))
axes = axes.flatten()
for i, col in enumerate(features):
    sns.histplot(df[col], kde=True, ax=axes[i], color=sns.color_palette("viridis")[i % 6])
    axes[i].set_title(col, fontsize=12, fontweight="bold")
# Hide the empty subplot
axes[-1].set_visible(False)
fig.suptitle("Feature Distributions", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "03_feature_distributions.png"))
plt.close()
print("  [OK] Saved: 03_feature_distributions.png")

# --- 2d. Boxplots by crop (for key features) ---
for col in ["N", "temperature", "ph", "rainfall"]:
    fig, ax = plt.subplots(figsize=(16, 6))
    sns.boxplot(data=df, x="label", y=col, palette="viridis", ax=ax)
    ax.set_title(f"{col} Distribution by Crop", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fname = f"04_boxplot_{col}.png"
    plt.savefig(os.path.join(CHART_DIR, fname))
    plt.close()
    print(f"  [OK] Saved: {fname}")


# ==================================================
# 3. PREPROCESSING
# ==================================================
print("\n" + "=" * 60)
print("3. PREPROCESSING")
print("=" * 60)

X = df[features]
y = df["label"]

# Train/Test split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"  Train set: {X_train.shape[0]} samples")
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
    cm = confusion_matrix(y_test, res["predictions"], labels=sorted(y.unique()))
    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=sorted(y.unique()),
                yticklabels=sorted(y.unique()), ax=ax)
    ax.set_title(f"Confusion Matrix - {name}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Predicted", fontsize=12)
    ax.set_ylabel("Actual", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    fname = f"05_confusion_matrix_{name.lower().replace(' ', '_')}.png"
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
plt.savefig(os.path.join(CHART_DIR, "06_accuracy_comparison.png"))
plt.close()
print("\n  [OK] Saved: 06_accuracy_comparison.png")

# --- Feature importance (Random Forest) ---
rf_model = results["Random Forest"]["model"]
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(range(len(features)), importances[indices], color=sns.color_palette("viridis", len(features)))
ax.set_xticks(range(len(features)))
ax.set_xticklabels([features[i] for i in indices], rotation=45, ha="right")
ax.set_title("Feature Importance (Random Forest)", fontsize=16, fontweight="bold")
ax.set_ylabel("Importance", fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "07_feature_importance.png"))
plt.close()
print("  [OK] Saved: 07_feature_importance.png")


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
