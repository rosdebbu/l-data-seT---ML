# ============================================================
# Tutorial 4 (T4): Performance Metrics in Python
# ============================================================
# Goal: Train a classifier (Random Forest) and evaluate its
# performance using Accuracy, Precision, Recall, F1-Score,
# Classification Report, and Confusion Matrix.
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sklearn imports for data split and scaling
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Model import (Classification)
from sklearn.ensemble import RandomForestClassifier

# Metrics imports
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# --------------------------------------------------
# Setup output directory for plots
# --------------------------------------------------
OUT_DIR = "t4_metrics_output"
os.makedirs(OUT_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")

# --------------------------------------------------
# Step 1: Load or Generate Dataset
# --------------------------------------------------
data_path = os.path.join("data", "Crop_recommendation.csv")

if os.path.exists(data_path):
    print("=" * 60)
    print(f"TUTORIAL 4: PERFORMANCE METRICS USING {os.path.basename(data_path)}")
    print("=" * 60)
    df = pd.read_csv(data_path)
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
else:
    print("=" * 60)
    print("TUTORIAL 4: DATASET NOT FOUND, CREATING SAMPLE DATA")
    print("=" * 60)
    np.random.seed(42)
    crops = ['rice', 'maize', 'chickpea', 'lentil', 'pomegranate']
    df = pd.DataFrame({
        'N': np.random.randint(10, 140, 300),
        'P': np.random.randint(5, 145, 300),
        'K': np.random.randint(15, 205, 300),
        'temperature': np.random.uniform(8, 43, 300),
        'humidity': np.random.uniform(14, 100, 300),
        'ph': np.random.uniform(3.5, 9.9, 300),
        'rainfall': np.random.uniform(20, 300, 300),
        'label': np.random.choice(crops, 300)
    })
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']

print(f"Dataset Shape: {df.shape}")
print(f"Unique Target Classes: {len(y.unique())} classes ({list(y.unique()[:5])}...)")

# --------------------------------------------------
# Step 2: Split and Scale Data
# --------------------------------------------------
# 80% train, 20% test with stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples:  {X_test.shape[0]}")

# --------------------------------------------------
# Step 3: Train Classifier
# --------------------------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Make predictions on unseen test data
y_pred = model.predict(X_test_scaled)

# --------------------------------------------------
# Step 4: Calculate Performance Metrics
# --------------------------------------------------
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

print("\n" + "=" * 50)
print("             T4 PERFORMANCE METRICS")
print("=" * 50)
print(f"  Accuracy:  {acc:.4f}  ({acc * 100:.2f}%)")
print(f"  Precision: {prec:.4f}")
print(f"  Recall:    {rec:.4f}")
print(f"  F1-Score:  {f1:.4f}")
print("=" * 50)

# --------------------------------------------------
# Step 5: Classification Report
# --------------------------------------------------
print("\nClassification Report (Per-Class Breakdown):")
print(classification_report(y_test, y_pred, zero_division=0))

# --------------------------------------------------
# Step 6: Plot Confusion Matrix Heatmap
# --------------------------------------------------
labels = sorted(y.unique())
cm = confusion_matrix(y_test, y_pred, labels=labels)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=labels, yticklabels=labels)
plt.title('Tutorial 4: Confusion Matrix (Random Forest)', fontsize=14, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=12)
plt.ylabel('Actual Label', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

cm_path = os.path.join(OUT_DIR, "confusion_matrix.png")
plt.savefig(cm_path, dpi=300)
plt.close()
print(f"[Saved] Confusion Matrix plot -> {cm_path}")

# --------------------------------------------------
# Step 7: Plot Metrics Bar Chart
# --------------------------------------------------
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
metrics_values = [acc, prec, rec, f1]

plt.figure(figsize=(8, 5))
bars = plt.bar(metrics_names, metrics_values, color=['#2b5c8f', '#4682b4', '#5f9ea0', '#2e8b57'])
plt.ylim(0, 1.1)
plt.title('Tutorial 4: Classification Performance Metrics', fontsize=14, fontweight='bold')
plt.ylabel('Score (0.0 to 1.0)', fontsize=12)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.02, f'{yval:.4f}',
             ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
bar_path = os.path.join(OUT_DIR, "metrics_bar_chart.png")
plt.savefig(bar_path, dpi=300)
plt.close()
print(f"[Saved] Metrics Bar Chart -> {bar_path}")

print("\nTutorial 4 execution completed successfully!")
