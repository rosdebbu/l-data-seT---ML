# ============================================================
# Tutorial 2 (T2): Linear Regression in Python
# ============================================================
# Goal: Build Linear Regression, Ridge & Lasso models to predict
# a continuous target (Rainfall / Moisture), evaluate metrics
# (MAE, MSE, RMSE, R2), and demonstrate Regularization.
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --------------------------------------------------
# Setup output directory for plots
# --------------------------------------------------
OUT_DIR = "t2_regression_output"
os.makedirs(OUT_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")

# Load dataset
data_path = os.path.join("data", "Crop_recommendation.csv")
if not os.path.exists(data_path):
    data_path = os.path.join("data", "Fertilizer_Prediction.csv")

print("=" * 60)
print(f"TUTORIAL 2: LINEAR REGRESSION USING {os.path.basename(data_path)}")
print("=" * 60)

df = pd.read_csv(data_path)

# --------------------------------------------------
# Step 1: Select Features and Continuous Target
# --------------------------------------------------
# We will predict 'rainfall' (or 'Moisture') using environmental features
if "rainfall" in df.columns:
    target_col = "rainfall"
    feature_cols = ["N", "P", "K", "temperature", "humidity", "ph"]
else:
    target_col = "Moisture"
    feature_cols = ["Temperature", "Humidity", "Nitrogen", "Phosphorous", "Potassium"]

print(f"\nTarget Variable (Continuous): {target_col}")
print(f"Feature Variables: {feature_cols}")

X = df[feature_cols]
y = df[target_col]

# --------------------------------------------------
# Step 2: Split and Scale Data
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --------------------------------------------------
# Step 3: Train Linear Regression, Ridge, and Lasso
# --------------------------------------------------
models = {
    "Linear Regression (OLS)": LinearRegression(),
    "Ridge Regression (L2)": Ridge(alpha=1.0),
    "Lasso Regression (L1)": Lasso(alpha=0.1)
}

print("\n" + "-" * 50)
print(f"{'Model':<25} {'MAE':>8} {'MSE':>8} {'RMSE':>8} {'R2 Score':>10}")
print("-" * 50)

predictions = {}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    predictions[name] = y_pred
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"{name:<25} {mae:>8.2f} {mse:>8.2f} {rmse:>8.2f} {r2:>10.4f}")

# --------------------------------------------------
# Step 4: Plots — Actual vs Predicted & Coefficients
# --------------------------------------------------
# 4a. Actual vs Predicted Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(y_test, predictions["Linear Regression (OLS)"], alpha=0.6, color='blue', label='Predictions')
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Ideal Line (y = x)')
ax.set_xlabel(f"Actual {target_col}")
ax.set_ylabel(f"Predicted {target_col}")
ax.set_title(f"Linear Regression: Actual vs Predicted {target_col}")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "actual_vs_predicted.png"))
plt.close()
print("\n  [OK] Saved plot: actual_vs_predicted.png")

# 4b. Regularization Feature Coefficients Comparison
lr_model = models["Linear Regression (OLS)"]
ridge_model = models["Ridge Regression (L2)"]
lasso_model = models["Lasso Regression (L1)"]

coef_df = pd.DataFrame({
    'Feature': feature_cols,
    'Linear Regression': lr_model.coef_,
    'Ridge (L2)': ridge_model.coef_,
    'Lasso (L1)': lasso_model.coef_
})

fig, ax = plt.subplots(figsize=(10, 5))
coef_df.set_index('Feature').plot(kind='bar', ax=ax)
ax.set_title("Feature Coefficients: Linear vs Ridge vs Lasso")
ax.set_ylabel("Coefficient Weight")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "coefficients_comparison.png"))
plt.close()
print("  [OK] Saved plot: coefficients_comparison.png")

print("\n" + "=" * 60)
print("TUTORIAL 2 COMPLETED SUCCESSFULLY!")
print("=" * 60)
