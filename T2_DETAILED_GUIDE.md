# Tutorial 2 (T2): Linear Regression & Regularization in Python — Detailed Guide

## What is This Tutorial About?

In Tutorial 1 (T1), we cleaned and preprocessed our agricultural data. Now in Tutorial 2 (T2), we actually **build a Machine Learning model** — specifically **Linear Regression** — to predict a **continuous numerical value**.

While our main crop recommendation project does **Classification** (predicting a crop *name*), this tutorial focuses on **Regression** — predicting a **number**. We predict how much **Rainfall** (in mm) a particular farm would need based on its soil nutrients and climate conditions.

We also explore **Regularization** (Ridge and Lasso) — techniques to prevent our model from memorizing noise in the data (overfitting).

---

## What is the Difference Between Classification and Regression?

| | Classification | Regression |
|---|---|---|
| **Output** | A category/label | A continuous number |
| **Example** | Crop = "Rice" or "Maize" | Rainfall = 202.5 mm |
| **Algorithm** | Random Forest, KNN, Decision Tree | Linear Regression, Ridge, Lasso |
| **Used in** | Crop Recommendation, Fertilizer Prediction | Predicting rainfall, temperature, moisture |

In this tutorial we do **Regression** because it teaches important concepts like the linear equation, error metrics, and regularization.

---

## Our Setup: Features and Target

### What are we predicting?

**Target variable (y):** `rainfall` — a continuous number (measured in mm).

### What inputs do we use to predict it?

**Feature variables (X):** Soil nutrients and climate conditions.

| Feature | What it Means | Example Value |
|---------|--------------|---------------|
| N | Nitrogen content in soil | 90 |
| P | Phosphorous content in soil | 42 |
| K | Potassium content in soil | 43 |
| temperature | Temperature in Celsius | 20.5 |
| humidity | Relative humidity in % | 82.0 |
| ph | pH value of soil | 6.5 |

**Question we're answering:** *"Given soil nutrients (N, P, K) and weather (temperature, humidity, pH), how much rainfall does this farm need?"*

### What We Did in the Code

```python
target_col = "rainfall"
feature_cols = ["N", "P", "K", "temperature", "humidity", "ph"]

X = df[feature_cols]   # 6 input features (200 rows x 6 columns)
y = df[target_col]     # 1 output target (200 rainfall values)
```

---

## Step 1: Train-Test Split & Feature Scaling

Before building any model, we first split and scale the data (same concept as T1).

### What We Did in the Code

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Split: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # Fit on train, transform train
X_test_scaled = scaler.transform(X_test)          # Only transform test (no fit!)
```

### Why `fit_transform` on Train but only `transform` on Test?

- **`fit_transform(X_train)`** = Learn the mean and std from training data, then scale it.
- **`transform(X_test)`** = Use the SAME mean and std learned from training to scale test data.

If we fit on test data too, we would leak test information into our model. This is called **data leakage** and gives fake accuracy.

---

## Step 2: What is Linear Regression?

### The Core Idea

Linear Regression finds the **best straight line** (or hyperplane in multiple dimensions) that maps input features to the output target.

### The Equation

```
rainfall = b0 + b1*(Nitrogen) + b2*(Phosphorous) + b3*(Potassium) 
              + b4*(temperature) + b5*(humidity) + b6*(pH)
```

Where:
- **b0** = intercept (the starting value when all features are 0)
- **b1, b2, ... b6** = coefficients/weights (how much each feature contributes)

### How Does it Learn?

The model tries many different values for b0, b1, b2... and picks the combination that makes the **total error** between predicted rainfall and actual rainfall as **small as possible**.

This error is measured by the **cost function** (Mean Squared Error):

```
Cost = (1/n) * sum of (actual_rainfall - predicted_rainfall)^2
```

The model minimizes this cost function using a mathematical technique called **Ordinary Least Squares (OLS)** — it directly calculates the optimal weights.

### What We Did in the Code

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train_scaled, y_train)        # Learn the weights from training data
y_pred = model.predict(X_test_scaled)     # Predict rainfall on test data
```

After fitting, the model stores:
- `model.intercept_` = b0 (the intercept)
- `model.coef_` = [b1, b2, b3, b4, b5, b6] (the 6 feature weights)

---

## Step 3: Evaluation Metrics — How Good is Our Prediction?

After the model predicts rainfall values, we need to measure **how far off** those predictions are from the real values.

### The 4 Metrics We Calculate

| Metric | What it Measures | Formula (Simple) | How to Interpret |
|--------|-----------------|-------------------|------------------|
| **MAE** (Mean Absolute Error) | Average error distance | Average of all \|actual - predicted\| | Lower is better. MAE = 10 means predictions are off by 10 mm on average |
| **MSE** (Mean Squared Error) | Average squared error | Average of (actual - predicted)^2 | Lower is better. Penalizes large errors much more than small ones |
| **RMSE** (Root Mean Squared Error) | Error in original units | Square root of MSE | Lower is better. RMSE = 15 means typical error is about 15 mm |
| **R2 Score** (R-squared) | How much variance is explained | 1 - (residual error / total variance) | Range 0 to 1. R2 = 0.85 means 85% of rainfall variation is explained by our features |

### What We Did in the Code

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, y_pred)      # Average absolute error
mse = mean_squared_error(y_test, y_pred)        # Average squared error
rmse = np.sqrt(mse)                             # Square root of MSE
r2 = r2_score(y_test, y_pred)                   # Proportion of variance explained
```

### Example Output

```
Model                     MAE      MSE     RMSE   R2 Score
--------------------------------------------------
Linear Regression (OLS)   74.04  6824.91    82.61    -0.1051
Ridge Regression (L2)     74.03  6824.11    82.61    -0.1050
Lasso Regression (L1)     74.02  6822.36    82.60    -0.1047
```

### How to Read This Output

- **MAE = 74.04:** On average, our rainfall prediction is off by 74 mm.
- **RMSE = 82.61:** The typical prediction error is about 82 mm.
- **R2 = -0.10:** The model explains very little variance in rainfall (this is expected because we're using random sample data — with the real Kaggle dataset, R2 would be much higher).

---

## Step 4: Regularization — Ridge (L2) and Lasso (L1)

### The Problem: Overfitting

Sometimes Linear Regression assigns **very large weights** to features, making the model too sensitive to small changes in training data. This is called **overfitting** — the model memorizes noise instead of learning real patterns.

### The Solution: Add a Penalty

Regularization adds an **extra cost** to the model for having large weights. This forces the model to keep weights small and simple.

### Ridge Regression (L2 Penalty)

Ridge adds a penalty equal to the **sum of squared weights**:

```
Total Cost = MSE + lambda * (w1^2 + w2^2 + w3^2 + w4^2 + w5^2 + w6^2)
```

- The model must now balance: making predictions accurate (low MSE) AND keeping weights small (low penalty).
- **Effect:** All weights get shrunk **smoothly** toward 0, but **none become exactly 0**. Every feature stays in the model.
- **lambda** controls the strength of the penalty (higher lambda = stronger shrinkage).

### Lasso Regression (L1 Penalty)

Lasso adds a penalty equal to the **sum of absolute weights**:

```
Total Cost = MSE + lambda * (|w1| + |w2| + |w3| + |w4| + |w5| + |w6|)
```

- **Effect:** Some weights get shrunk to **exactly 0**, effectively **removing** those features from the model.
- This means Lasso performs **automatic feature selection** — it tells you which features are useless!

### What We Did in the Code

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso

models = {
    "Linear Regression (OLS)": LinearRegression(),       # No penalty
    "Ridge Regression (L2)":   Ridge(alpha=1.0),          # L2 penalty, lambda=1.0
    "Lasso Regression (L1)":   Lasso(alpha=0.1),          # L1 penalty, lambda=0.1
}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    # ... calculate MAE, MSE, RMSE, R2 ...
```

### Before vs After Regularization (Coefficient Weights Example)

```
Feature       Linear Reg    Ridge (L2)    Lasso (L1)
---------     ----------    ----------    ----------
Nitrogen         2.50          2.10          1.80
Phosphorous      0.80          0.70          0.00  <-- Lasso dropped it!
Potassium        1.30          1.10          0.90
temperature     -0.50         -0.45         -0.30
humidity         3.20          2.80          2.50
pH              -1.20         -1.00         -0.80
```

Notice how:
- **Ridge** shrinks ALL weights (2.50 → 2.10, 0.80 → 0.70) but keeps every feature.
- **Lasso** shrinks some weights AND drops Phosphorous to **exactly 0.00** — telling us Phosphorous doesn't help predict rainfall!

---

## Step 5: Visualization — The Two Plots We Generated

### Plot 1: Actual vs Predicted Rainfall

This scatter plot shows every test sample:
- **X-axis:** Actual rainfall value from the dataset.
- **Y-axis:** Rainfall value predicted by our model.
- **Red dashed line:** The ideal line (y = x). If predictions were perfect, every point would sit exactly on this line.
- **Blue dots far from the red line** = big prediction errors.

```python
ax.scatter(y_test, predictions["Linear Regression (OLS)"], color='blue', label='Predictions')
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Ideal Line')
```

### Plot 2: Feature Coefficients Comparison

This bar chart shows the **weight/importance** each feature received from each model:
- Tall bars = important features (high weight).
- Bars near 0 = unimportant features.
- Compares Linear Regression vs Ridge vs Lasso side-by-side.

```python
coef_df = pd.DataFrame({
    'Feature': feature_cols,
    'Linear Regression': lr_model.coef_,
    'Ridge (L2)': ridge_model.coef_,
    'Lasso (L1)': lasso_model.coef_
})
coef_df.set_index('Feature').plot(kind='bar')
```

---

## Bias-Variance Tradeoff (The Core ML Concept Behind T2)

### What is Bias?

- **Bias** = error from making the model **too simple**.
- A model with high bias **underfits** — it cannot capture the true patterns.
- Example: Using a straight line to predict data that actually curves.

### What is Variance?

- **Variance** = error from making the model **too sensitive** to training data.
- A model with high variance **overfits** — it memorizes noise.
- Example: The model changes drastically when you add or remove a few data points.

### The Tradeoff

```
Total Error = Bias^2 + Variance + Irreducible Noise

You cannot minimize both simultaneously:
  - Make model MORE complex --> Bias goes DOWN, Variance goes UP
  - Make model LESS complex --> Bias goes UP, Variance goes DOWN
```

### How Regularization Helps

| Technique | What it Does | Effect on Bias | Effect on Variance |
|-----------|-------------|----------------|-------------------|
| No Regularization (OLS) | No penalty on weights | Low bias | Potentially high variance (overfitting) |
| Ridge (L2) | Shrinks weights smoothly | Slightly increases bias | Reduces variance |
| Lasso (L1) | Drops unimportant weights to 0 | Slightly increases bias | Reduces variance significantly |

Regularization intentionally adds a small amount of bias to get a much larger reduction in variance — resulting in a **better overall model**.

---

## Complete Data Flow Summary

```
CROP RECOMMENDATION CSV (200 rows x 8 columns)
    |
    | Select features (N, P, K, temp, humidity, pH) and target (rainfall)
    v
X (200 x 6 feature matrix)  +  y (200 rainfall values)
    |
    | train_test_split(test_size=0.2)
    v
X_train (160 x 6)  X_test (40 x 6)  y_train (160)  y_test (40)
    |
    | StandardScaler: fit on train, transform both
    v
X_train_scaled (160 x 6)  X_test_scaled (40 x 6)
    |
    | Train 3 models:
    |   1. LinearRegression()    -- No penalty
    |   2. Ridge(alpha=1.0)      -- L2 penalty
    |   3. Lasso(alpha=0.1)      -- L1 penalty
    v
y_pred (40 predicted rainfall values)
    |
    | Compare y_pred vs y_test:
    v
METRICS: MAE, MSE, RMSE, R2 Score
PLOTS:   actual_vs_predicted.png, coefficients_comparison.png
```

---

## What I Learned from Tutorial 2 (Write This in Your Notebook)

1. **Linear Regression** is a supervised parametric model that predicts continuous numerical outputs by fitting the equation $y = b_0 + b_1 X_1 + ... + b_n X_n$. We used it to predict rainfall requirements from soil nutrient and climate features.

2. **Evaluation Metrics** quantify model performance: MAE measures average prediction error in original units, RMSE penalizes large errors, and R2 Score measures the proportion of target variance explained by input features (0 to 1, higher is better).

3. **Regularization** prevents overfitting by penalizing large feature weights. **Ridge (L2)** adds a squared-weight penalty that shrinks all coefficients smoothly. **Lasso (L1)** adds an absolute-weight penalty that can shrink uninformative coefficients to exactly zero, performing automatic feature selection.

4. **Bias-Variance Tradeoff** is the fundamental tension in ML: too simple models underfit (high bias), too complex models overfit (high variance). Regularization balances this tradeoff by intentionally adding a small amount of bias to achieve a much larger reduction in variance.
