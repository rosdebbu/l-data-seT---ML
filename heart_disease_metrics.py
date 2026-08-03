"""
=============================================================
  Heart Disease Prediction -- Classification Metrics
=============================================================
  Dataset : Heart Disease UCI (Kaggle)
  Model   : Logistic Regression
  Metrics : Accuracy, Precision, Recall, F1 Score
  
  Kaggle Link: https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
=============================================================
"""

# ---------------------------------------------------------------
# STEP 1: Import Libraries
# ---------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import warnings
warnings.filterwarnings('ignore')

print("[OK] All libraries imported successfully!\n")

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output_charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# STEP 2: Load the Heart Disease Dataset
# ─────────────────────────────────────────────────────────────
csv_path = os.path.join(SCRIPT_DIR, "heart_disease_data.csv")
df = pd.read_csv(csv_path)

print("=" * 60)
print("  📊 HEART DISEASE DATASET — Overview")
print("=" * 60)
print(f"\n  Shape       : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  Features    : {df.shape[1] - 1}")
print(f"  Target      : 'target' (1 = Heart Disease, 0 = No Disease)")
print()

# ─────────────────────────────────────────────────────────────
# STEP 3: Explore the Dataset
# ─────────────────────────────────────────────────────────────
print("─" * 60)
print("  FIRST 5 ROWS OF THE DATASET")
print("─" * 60)
print(df.head().to_string())
print()

print("─" * 60)
print("  DATASET STATISTICS")
print("─" * 60)
print(df.describe().to_string())
print()

print("─" * 60)
print("  MISSING VALUES")
print("─" * 60)
print(f"  Total missing values: {df.isnull().sum().sum()}")
print()

print("─" * 60)
print("  CLASS DISTRIBUTION (Target)")
print("─" * 60)
target_counts = df['target'].value_counts()
print(f"  1 (Heart Disease)   : {target_counts.get(1, 0)} patients")
print(f"  0 (No Heart Disease): {target_counts.get(0, 0)} patients")
print()

# ─────────────────────────────────────────────────────────────
# STEP 4: Feature Description
# ─────────────────────────────────────────────────────────────
print("─" * 60)
print("  📋 FEATURE DESCRIPTIONS")
print("─" * 60)
features_info = {
    'age': 'Age of the patient (years)',
    'sex': 'Sex (1 = Male, 0 = Female)',
    'cp': 'Chest Pain type (0-3)',
    'trestbps': 'Resting Blood Pressure (mm Hg)',
    'chol': 'Cholesterol level (mg/dl)',
    'fbs': 'Fasting Blood Sugar > 120 mg/dl (1=True, 0=False)',
    'restecg': 'Resting ECG results (0-2)',
    'thalach': 'Maximum Heart Rate achieved',
    'exang': 'Exercise Induced Angina (1=Yes, 0=No)',
    'oldpeak': 'ST Depression induced by exercise',
    'slope': 'Slope of peak exercise ST segment',
    'ca': 'Number of major vessels colored by fluoroscopy (0-4)',
    'thal': 'Thalassemia (1=Normal, 2=Fixed Defect, 3=Reversible Defect)',
    'target': '1 = Has Heart Disease, 0 = No Heart Disease'
}
for feat, desc in features_info.items():
    print(f"  {feat:10s} → {desc}")
print()

# ─────────────────────────────────────────────────────────────
# STEP 5: Visualize the Data
# ─────────────────────────────────────────────────────────────
# Chart 1: Class Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

colors_target = ['#FF6B6B', '#4ECDC4']
labels = ['No Disease (0)', 'Heart Disease (1)']
target_counts_sorted = df['target'].value_counts().sort_index()
axes[0].bar(labels, target_counts_sorted.values, color=colors_target, edgecolor='black', linewidth=1.2)
axes[0].set_title('Target Class Distribution', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Count', fontsize=12)
for i, v in enumerate(target_counts_sorted.values):
    axes[0].text(i, v + 2, str(v), ha='center', fontweight='bold', fontsize=13)

# Chart 2: Age distribution by target
for i, label in enumerate([0, 1]):
    subset = df[df['target'] == label]
    axes[1].hist(subset['age'], bins=15, alpha=0.6, label=labels[i], 
                 color=colors_target[i], edgecolor='black')
axes[1].set_title('Age Distribution by Heart Disease', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Age', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)
axes[1].legend(fontsize=11)

plt.tight_layout()
chart1_path = os.path.join(OUTPUT_DIR, "01_data_exploration.png")
plt.savefig(chart1_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"  📈 Chart saved: {chart1_path}")

# ─────────────────────────────────────────────────────────────
# STEP 6: Prepare the Data (Train-Test Split)
# ─────────────────────────────────────────────────────────────
# Separate features (X) and target (y)
X = df.drop('target', axis=1)
y = df['target']

# Scale the features for better model performance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print()
print("─" * 60)
print("  🔀 TRAIN-TEST SPLIT")
print("─" * 60)
print(f"  Training set : {X_train.shape[0]} samples (80%)")
print(f"  Testing set  : {X_test.shape[0]} samples (20%)")
print()

# ─────────────────────────────────────────────────────────────
# STEP 7: Train the Logistic Regression Model
# ─────────────────────────────────────────────────────────────
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

print("─" * 60)
print("  🤖 MODEL TRAINING")
print("─" * 60)
print("  ✅ Logistic Regression model trained successfully!")
print(f"\n  Predictions : {y_pred}")
print(f"  Actual      : {y_test.values}")
print()

# ─────────────────────────────────────────────────────────────
# STEP 8: Calculate ALL 4 Classification Metrics
# ─────────────────────────────────────────────────────────────

# 1. ACCURACY
accuracy = accuracy_score(y_test, y_pred)

# 2. PRECISION
precision = precision_score(y_test, y_pred)

# 3. RECALL
recall = recall_score(y_test, y_pred)

# 4. F1 SCORE
f1 = f1_score(y_test, y_pred)

print("=" * 60)
print("  🎯 CLASSIFICATION METRICS RESULTS")
print("=" * 60)
print()
print(f"  📌 Accuracy   = {accuracy:.4f}   ({accuracy*100:.2f}%)")
print(f"  📌 Precision  = {precision:.4f}   ({precision*100:.2f}%)")
print(f"  📌 Recall     = {recall:.4f}   ({recall*100:.2f}%)")
print(f"  📌 F1 Score   = {f1:.4f}   ({f1*100:.2f}%)")
print()
print("=" * 60)

# ─────────────────────────────────────────────────────────────
# STEP 9: What Do These Metrics Mean? (Formulas)
# ─────────────────────────────────────────────────────────────
print()
print("─" * 60)
print("  📖 METRIC FORMULAS & MEANINGS")
print("─" * 60)
print("""
  ┌────────────┬─────────────────────────────────────────────────────────┐
  │ Metric     │ Formula & Meaning                                      │
  ├────────────┼─────────────────────────────────────────────────────────┤
  │ Accuracy   │ (TP + TN) / Total                                      │
  │            │ → Overall correctness of the model                      │
  ├────────────┼─────────────────────────────────────────────────────────┤
  │ Precision  │ TP / (TP + FP)                                         │
  │            │ → When model says "Disease", how often is it correct?   │
  ├────────────┼─────────────────────────────────────────────────────────┤
  │ Recall     │ TP / (TP + FN)                                         │
  │            │ → Of all actual Disease patients, how many did we find? │
  ├────────────┼─────────────────────────────────────────────────────────┤
  │ F1 Score   │ 2 × (Precision × Recall) / (Precision + Recall)        │
  │            │ → Balance between Precision and Recall                  │
  └────────────┴─────────────────────────────────────────────────────────┘

  Where: TP = True Positive, TN = True Negative,
         FP = False Positive, FN = False Negative
""")

# ─────────────────────────────────────────────────────────────
# STEP 10: Detailed Classification Report
# ─────────────────────────────────────────────────────────────
print("─" * 60)
print("  📋 DETAILED CLASSIFICATION REPORT (Per-Class)")
print("─" * 60)
print(classification_report(
    y_test, y_pred,
    target_names=['No Disease (0)', 'Heart Disease (1)']
))

# ─────────────────────────────────────────────────────────────
# STEP 11: Confusion Matrix (Chart)
# ─────────────────────────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)

fig, ax = plt.subplots(figsize=(8, 6))
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=['No Disease', 'Heart Disease']
)
disp.plot(cmap='Blues', ax=ax, values_format='d')
ax.set_title('Confusion Matrix — Logistic Regression\nHeart Disease Dataset',
             fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
chart2_path = os.path.join(OUTPUT_DIR, "02_confusion_matrix.png")
plt.savefig(chart2_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"  📈 Chart saved: {chart2_path}")

# Print confusion matrix values
tn, fp, fn, tp = cm.ravel()
print(f"""
  ┌─────────────────────────────────────┐
  │       CONFUSION MATRIX VALUES       │
  ├─────────────────────────────────────┤
  │  True Negatives  (TN) = {tn:3d}        │
  │  False Positives (FP) = {fp:3d}        │
  │  False Negatives (FN) = {fn:3d}        │
  │  True Positives  (TP) = {tp:3d}        │
  └─────────────────────────────────────┘
""")

# ─────────────────────────────────────────────────────────────
# STEP 12: Bar Chart — Compare All 4 Metrics
# ─────────────────────────────────────────────────────────────
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
metrics_values = [accuracy, precision, recall, f1]
bar_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(metrics_names, metrics_values, color=bar_colors,
              edgecolor='black', linewidth=1.2, width=0.6)

# Add value labels on top of each bar
for bar, val in zip(bars, metrics_values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{val:.4f}\n({val*100:.1f}%)', ha='center', va='bottom',
            fontsize=12, fontweight='bold')

ax.set_ylim(0, 1.2)
ax.set_ylabel('Score', fontsize=13)
ax.set_title('Classification Metrics — Logistic Regression\nHeart Disease Prediction',
             fontsize=15, fontweight='bold', pad=15)
ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Perfect Score (1.0)')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
chart3_path = os.path.join(OUTPUT_DIR, "03_metrics_comparison.png")
plt.savefig(chart3_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"  📈 Chart saved: {chart3_path}")

# ─────────────────────────────────────────────────────────────
# STEP 13: Final Summary Table
# ─────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("  📊 FINAL SUMMARY — Heart Disease Classification Metrics")
print("  Dataset: Heart Disease UCI  |  Model: Logistic Regression")
print("  Training: 80%  |  Testing: 20%")
print("=" * 70)

summary_df = pd.DataFrame({
    'Metric': ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
    'Score': [f'{v:.4f}' for v in metrics_values],
    'Percentage': [f'{v*100:.2f}%' for v in metrics_values],
    'Meaning': [
        'Overall correctness of the model',
        'When predicting disease, how often correct?',
        'Of actual patients, how many did we find?',
        'Harmonic mean of Precision & Recall'
    ]
})
print()
print(summary_df.to_string(index=False))
print()
print("=" * 70)
print(f"\n  📁 All charts saved in: {OUTPUT_DIR}")
print("  ✅ DONE! All metrics calculated successfully.\n")
