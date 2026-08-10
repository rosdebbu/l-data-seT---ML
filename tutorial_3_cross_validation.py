# ============================================================
# Tutorial 3 (T3): Cross Validation & Learning Curves in Python
# ============================================================
# Goal: Implement K-Fold Cross Validation (5-Fold and 10-Fold),
# plot Learning Curves, and analyze Overfitting, Underfitting,
# and Bias-Variance tradeoff.
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score, learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# --------------------------------------------------
# Setup output directory for plots
# --------------------------------------------------
OUT_DIR = "t3_crossval_output"
os.makedirs(OUT_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")

# Load dataset
data_path = os.path.join("data", "Crop_recommendation.csv")
if not os.path.exists(data_path):
    data_path = os.path.join("data", "Fertilizer_Prediction.csv")

print("=" * 60)
print(f"TUTORIAL 3: CROSS VALIDATION USING {os.path.basename(data_path)}")
print("=" * 60)

df = pd.read_csv(data_path)

# Prepare Features (X) and Target (y)
if "label" in df.columns:
    X = df.drop(columns=["label"])
    y = df["label"]
else:
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    X = df.drop(columns=cat_cols)
    y = df["Fertilizer Name"] if "Fertilizer Name" in df.columns else df.iloc[:, -1]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --------------------------------------------------
# Step 1: K-Fold Cross Validation (5-Fold & 10-Fold)
# --------------------------------------------------
print("\n[Step 1] K-Fold Cross Validation Evaluation")

model = RandomForestClassifier(n_estimators=50, random_state=42)

for k in [5, 10]:
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_scaled, y, cv=skf, scoring='accuracy')
    
    print(f"\n{k}-Fold Stratified Cross Validation Results:")
    print(f"  Scores for each fold: {np.round(scores, 4)}")
    print(f"  Mean Accuracy: {scores.mean():.4f} ({scores.mean()*100:.2f}%)")
    print(f"  Standard Deviation (Variance): {scores.std():.4f}")

# --------------------------------------------------
# Step 2: Learning Curve Plot (Diagnosing Bias vs Variance)
# --------------------------------------------------
print("\n[Step 2] Generating Learning Curve...")

train_sizes, train_scores, val_scores = learning_curve(
    estimator=model,
    X=X_scaled,
    y=y,
    train_sizes=np.linspace(0.1, 1.0, 10),
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

train_mean = np.mean(train_scores, axis=1)
train_std  = np.std(train_scores, axis=1)
val_mean   = np.mean(val_scores, axis=1)
val_std    = np.std(val_scores, axis=1)

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(train_sizes, train_mean, 'o-', color='blue', label='Training Score')
ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.15, color='blue')

ax.plot(train_sizes, val_mean, 's-', color='green', label='Validation Score (Cross-Val)')
ax.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.15, color='green')

ax.set_title("Learning Curve (Diagnosing Overfitting vs Underfitting)", fontsize=14, fontweight='bold')
ax.set_xlabel("Number of Training Samples")
ax.set_ylabel("Accuracy Score")
ax.set_ylim(0, 1.05)
ax.legend(loc='lower right')
plt.tight_layout()

plt.savefig(os.path.join(OUT_DIR, "learning_curve.png"))
plt.close()
print("  [OK] Saved plot: learning_curve.png")

print("\n" + "=" * 60)
print("TUTORIAL 3 COMPLETED SUCCESSFULLY!")
print("=" * 60)
