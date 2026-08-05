"""
=============================================================
  Diabetes Prediction -- Classification Metrics
=============================================================
  Dataset : Pima Indians Diabetes (Kaggle / UCI)
  Model   : Logistic Regression
  Metrics : Accuracy, Precision, Recall, F1 Score
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

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output_charts_diabetes")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# STEP 2: Load the Diabetes Dataset
# ─────────────────────────────────────────────────────────────
csv_path = os.path.join(SCRIPT_DIR, "diabetes_data.csv")
df = pd.read_csv(csv_path)

print("=" * 60)
print("  📊 DIABETES DATASET — Overview")
print("=" * 60)
print(f"\n  Shape       : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  Features    : {df.shape[1] - 1}")
print(f"  Target      : 'Outcome' (1 = Has Diabetes, 0 = No Diabetes)")
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
print("  CLASS DISTRIBUTION (Target)")
print("─" * 60)
target_counts = df['Outcome'].value_counts()
print(f"  1 (Has Diabetes) : {target_counts.get(1, 0)} patients")
print(f"  0 (No Diabetes)  : {target_counts.get(0, 0)} patients")
print()

# ─────────────────────────────────────────────────────────────
# STEP 4: Visualize Data
# ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

colors_target = ['#FF6B6B', '#4ECDC4']
labels = ['No Diabetes (0)', 'Has Diabetes (1)']
target_counts_sorted = df['Outcome'].value_counts().sort_index()
axes[0].bar(labels, target_counts_sorted.values, color=colors_target, edgecolor='black', linewidth=1.2)
axes[0].set_title('Target Class Distribution', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Count', fontsize=12)
for i, v in enumerate(target_counts_sorted.values):
    axes[0].text(i, v + 5, str(v), ha='center', fontweight='bold', fontsize=13)

for i, label in enumerate([0, 1]):
    subset = df[df['Outcome'] == label]
    axes[1].hist(subset['Glucose'], bins=15, alpha=0.6, label=labels[i],
                 color=colors_target[i], edgecolor='black')
axes[1].set_title('Glucose Level by Diabetes Outcome', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Glucose Level', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)
axes[1].legend(fontsize=11)

plt.tight_layout()
chart1_path = os.path.join(OUTPUT_DIR, "01_data_exploration.png")
plt.savefig(chart1_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"  📈 Chart saved: {chart1_path}")

# ─────────────────────────────────────────────────────────────
# STEP 5: Prepare Data (Train-Test Split)
# ─────────────────────────────────────────────────────────────
X = df.drop('Outcome', axis=1)
y = df['Outcome']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

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
# STEP 6: Train Model
# ─────────────────────────────────────────────────────────────
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# ─────────────────────────────────────────────────────────────
# STEP 7: Calculate Evaluation Metrics (Accuracy, Precision, Recall, F1)
# ─────────────────────────────────────────────────────────────
accuracy  = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall    = recall_score(y_test, y_pred)
f1        = f1_score(y_test, y_pred)

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

# Confusion Matrix Chart
cm = confusion_matrix(y_test, y_pred)

fig, ax = plt.subplots(figsize=(8, 6))
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=['No Diabetes', 'Diabetes']
)
disp.plot(cmap='Blues', ax=ax, values_format='d')
ax.set_title('Confusion Matrix — Logistic Regression\nDiabetes Dataset',
             fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
chart2_path = os.path.join(OUTPUT_DIR, "02_confusion_matrix.png")
plt.savefig(chart2_path, dpi=150, bbox_inches='tight')
plt.close()

# Bar Chart
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
metrics_values = [accuracy, precision, recall, f1]
bar_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(metrics_names, metrics_values, color=bar_colors,
              edgecolor='black', linewidth=1.2, width=0.6)

for bar, val in zip(bars, metrics_values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{val:.4f}\n({val*100:.1f}%)', ha='center', va='bottom',
            fontsize=12, fontweight='bold')

ax.set_ylim(0, 1.2)
ax.set_ylabel('Score', fontsize=13)
ax.set_title('Classification Metrics — Logistic Regression\nDiabetes Prediction',
             fontsize=15, fontweight='bold', pad=15)
ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Perfect Score (1.0)')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
chart3_path = os.path.join(OUTPUT_DIR, "03_metrics_comparison.png")
plt.savefig(chart3_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"  📈 All charts saved in: {OUTPUT_DIR}")
print("  ✅ DONE! All 4 metrics calculated successfully.\n")
