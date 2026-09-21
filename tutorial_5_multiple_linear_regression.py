# ============================================================
# Tutorial 5 (T5): Multiple Linear Regression in Python
# ============================================================
# Goal: Build a Multiple Linear Regression model using multiple
# input features (N, P, K, temperature, humidity, pH) to predict
# a continuous target (rainfall), and evaluate with MAE, MSE,
# RMSE, and R2 score.
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sklearn imports for data split and scaling
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Model import (Linear Regression)
from sklearn.linear_model import LinearRegression

# Regression metrics imports
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --------------------------------------------------
# Setup output directory for plots
# --------------------------------------------------
OUT_DIR = "t5_regression_output"
os.makedirs(OUT_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")

# --------------------------------------------------
# Step 1: Load or Generate Dataset
# --------------------------------------------------
data_path = os.path.join("data", "Crop_recommendation.csv")

if os.path.exists(data_path):
    print("=" * 60)
    print(f"TUTORIAL 5: MULTIPLE LINEAR REGRESSION USING {os.path.basename(data_path)}")
    print("=" * 60)
    df = pd.read_csv(data_path)
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph']
    target_col = 'rainfall'
    X = df[feature_cols]
    y = df[target_col]
else:
    print("=" * 60)
    print("TUTORIAL 5: DATASET NOT FOUND, CREATING SAMPLE DATA")
    print("=" * 60)
    np.random.seed(42)
    df = pd.DataFrame({
        'N': np.random.randint(10, 140, 300),
        'P': np.random.randint(5, 145, 300),
        'K': np.random.randint(15, 205, 300),
        'temperature': np.random.uniform(8, 43, 300),
        'humidity': np.random.uniform(14, 100, 300),
        'ph': np.random.uniform(3.5, 9.9, 300),
        'rainfall': np.random.uniform(20, 300, 300),
    })
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph']
    target_col = 'rainfall'
    X = df[feature_cols]
    y = df[target_col]

print(f"Features (X): {feature_cols}")
print(f"Target (y):   {target_col}")
print(f"Dataset Shape: {X.shape[0]} samples, {X.shape[1]} input features")

# --------------------------------------------------
# Step 2: Split and Scale Data
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples:  {X_test.shape[0]}")

# --------------------------------------------------
# Step 3: Fit Multiple Linear Regression Model
# --------------------------------------------------
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Inspect Intercept and Coefficients
print("\n" + "=" * 50)
print("       MULTIPLE LINEAR REGRESSION EQUATION")
print("=" * 50)
print(f"Intercept (b0): {model.intercept_:.4f}")
print("Feature Coefficients (Weights):")
for feat, coef in zip(feature_cols, model.coef_):
    print(f"  {feat:>12}: {coef:>9.4f}")
print("=" * 50)

# --------------------------------------------------
# Step 4: Make Predictions and Evaluate Metrics
# --------------------------------------------------
y_pred = model.predict(X_test_scaled)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n" + "=" * 50)
print("             T5 REGRESSION METRICS")
print("=" * 50)
print(f"  MAE  (Mean Absolute Error):     {mae:.4f}")
print(f"  MSE  (Mean Squared Error):      {mse:.4f}")
print(f"  RMSE (Root Mean Squared Error): {rmse:.4f}")
print(f"  R2   (R-Squared Score):         {r2:.4f}")
print("=" * 50)

# --------------------------------------------------
# Step 5: Plot Actual vs Predicted Scatter Plot
# --------------------------------------------------
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='#1f77b4', alpha=0.6, edgecolors='k', label='Predicted Points')
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', linewidth=2, label='Ideal Fit (y = x)')
plt.title('Tutorial 5: Actual vs Predicted Rainfall', fontsize=14, fontweight='bold')
plt.xlabel('Actual Rainfall (mm)', fontsize=12)
plt.ylabel('Predicted Rainfall (mm)', fontsize=12)
plt.legend()
plt.tight_layout()

scatter_path = os.path.join(OUT_DIR, "actual_vs_predicted.png")
plt.savefig(scatter_path, dpi=300)
plt.close()
print(f"[Saved] Actual vs Predicted Plot -> {scatter_path}")

# --------------------------------------------------
# Step 6: Plot Feature Coefficients Bar Chart
# --------------------------------------------------
plt.figure(figsize=(8, 5))
colors = ['#2ca02c' if c >= 0 else '#d62728' for c in model.coef_]
plt.barh(feature_cols, model.coef_, color=colors)
plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
plt.title('Tutorial 5: Feature Coefficients (Impact on Rainfall)', fontsize=14, fontweight='bold')
plt.xlabel('Coefficient Value (Weight)', fontsize=12)
plt.ylabel('Feature', fontsize=12)
plt.tight_layout()

coef_path = os.path.join(OUT_DIR, "feature_coefficients.png")
plt.savefig(coef_path, dpi=300)
plt.close()
print(f"[Saved] Coefficients Bar Chart -> {coef_path}")

print("\nTutorial 5 execution completed successfully!")
