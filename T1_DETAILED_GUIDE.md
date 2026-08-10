# Tutorial 1 (T1): Data Preprocessing in Python — Detailed Guide

## What is This Tutorial About?

In this tutorial, we take two raw agricultural datasets — **Crop Recommendation** and **Fertilizer Prediction** — and prepare them so that Machine Learning models can actually use them. Raw data has text strings, different number ranges, and potentially missing values. ML algorithms cannot work with any of that directly. So we **preprocess** the data first.

**The 4 preprocessing steps we perform:**
1. Data Inspection & Cleaning
2. Categorical Encoding (Text to Numbers)
3. Feature Scaling (Equalizing Number Ranges)
4. Train-Test Splitting (80% for Learning, 20% for Testing)

---

## Our Datasets

### Dataset 1: Crop Recommendation

This dataset helps predict which crop to grow based on soil and weather conditions.

| Column | What it Contains | Type |
|--------|-----------------|------|
| N | Nitrogen content in soil | Number (0 to 140) |
| P | Phosphorous content in soil | Number (5 to 145) |
| K | Potassium content in soil | Number (15 to 205) |
| temperature | Temperature in Celsius | Number (8.0 to 43.0) |
| humidity | Relative humidity in % | Number (14.0 to 100.0) |
| ph | pH value of soil | Number (3.5 to 9.9) |
| rainfall | Rainfall in mm | Number (20.0 to 300.0) |
| label | **Crop name (TARGET)** | Text (rice, maize, chickpea, etc.) |

### Dataset 2: Fertilizer Prediction

This dataset helps predict which fertilizer to use.

| Column | What it Contains | Type |
|--------|-----------------|------|
| Temperature | Temperature | Number |
| Humidity | Humidity % | Number |
| Moisture | Soil moisture | Number |
| Soil Type | Type of soil | **Text** (Clayey, Sandy, Loamy, etc.) |
| Crop Type | Type of crop | **Text** (Maize, Cotton, Wheat, etc.) |
| Nitrogen | Nitrogen level | Number |
| Phosphorous | Phosphorous level | Number |
| Potassium | Potassium level | Number |
| Fertilizer Name | **Fertilizer (TARGET)** | **Text** (Urea, DAP, etc.) |

Notice that the Fertilizer dataset has **3 text columns** (Soil Type, Crop Type, Fertilizer Name). These need to be converted to numbers before any ML model can use them.

---

## Step 1: Data Inspection & Cleaning

### What is Data Inspection?

Before doing anything, we first look at the data to understand:
- **How big is it?** (How many rows and columns?)
- **What types of data does it contain?** (Numbers? Text?)
- **Are there any missing values?** (Empty cells that could crash our model?)

### What We Did in the Code

```python
# Load the CSV files into pandas DataFrames
df_crop = pd.read_csv("data/Crop_recommendation.csv")
df_fert = pd.read_csv("data/Fertilizer_Prediction.csv")

# Check the shape (rows x columns)
print(df_crop.shape)   # Output: (200, 8)  --> 200 soil samples, 8 columns
print(df_fert.shape)   # Output: (200, 9)  --> 200 soil samples, 9 columns

# Check for missing values in every column
print(df_crop.isnull().sum())
print(df_fert.isnull().sum())
```

### What the Output Tells Us

```
Missing values in Crop Dataset:
N              0
P              0
K              0
temperature    0
humidity       0
ph             0
rainfall       0
label          0
```

**Result:** Every column shows `0` missing values. Our data is complete and clean — no rows need to be dropped or filled.

### Why is This Important?

- If there were missing values, the model would either crash or produce wrong results.
- Common fixes for missing data: **Drop the row** (`df.dropna()`) or **Fill with the average** (`df.fillna(df.mean())`).
- In our case, the data is already clean, so no filling or dropping is needed.

---

## Step 2: Categorical Encoding (Converting Text to Numbers)

### The Problem

Look at the Fertilizer dataset — it has columns like:
```
Soil Type:       "Clayey", "Sandy", "Loamy", "Black", "Red"
Crop Type:       "Maize", "Sugarcane", "Cotton", "Wheat"
Fertilizer Name: "Urea", "DAP", "14-35-14", "28-28"
```

Machine Learning models do **math** (matrix multiplication, distance calculations). You cannot do math on the word `"Clayey"`. The computer doesn't know if `"Clayey"` is bigger, smaller, or closer to `"Sandy"`.

### The Solution: LabelEncoder

`LabelEncoder` from scikit-learn converts each unique text value into a unique integer:

```
"Black"  --> 0
"Clayey" --> 1
"Loamy"  --> 2
"Red"    --> 3
"Sandy"  --> 4
```

### What We Did in the Code

```python
from sklearn.preprocessing import LabelEncoder

le_soil = LabelEncoder()
le_crop = LabelEncoder()
le_fert = LabelEncoder()

# Convert text to numbers
df_fert['Soil Type_encoded'] = le_soil.fit_transform(df_fert['Soil Type'])
df_fert['Crop Type_encoded'] = le_crop.fit_transform(df_fert['Crop Type'])
df_fert['Fertilizer_encoded'] = le_fert.fit_transform(df_fert['Fertilizer Name'])
```

### Before and After

| Soil Type (Before) | Soil Type_encoded (After) |
|---|---|
| Black | 0 |
| Clayey | 1 |
| Loamy | 2 |
| Red | 3 |
| Sandy | 4 |

Now the ML model can compute distances and matrix multiplications using these integer values.

### Why is This Important?

- Without encoding, algorithms like KNN, Random Forest, and Linear Regression **cannot process the data at all**.
- `LabelEncoder` is simple and efficient for tree-based models (Decision Tree, Random Forest).
- For models that might assume ordinal relationships between numbers (like Linear Regression), `OneHotEncoder` (creating separate binary 0/1 columns) is preferred. But for our classification project, `LabelEncoder` works perfectly.

---

## Step 3: Feature Scaling (Equalizing Number Ranges)

### The Problem

Look at the number ranges of our Crop dataset features:

| Feature | Minimum Value | Maximum Value | Range |
|---------|-------------|-------------|-------|
| Nitrogen (N) | 0 | 140 | 140 |
| Phosphorous (P) | 5 | 145 | 140 |
| Potassium (K) | 15 | 205 | 190 |
| temperature | 8.0 | 43.0 | 35 |
| humidity | 14.0 | 100.0 | 86 |
| **pH** | **3.5** | **9.9** | **6.4** |
| rainfall | 20.0 | 300.0 | 280 |

Notice that **Nitrogen ranges from 0-140**, but **pH only ranges from 3.5-9.9**. Potassium goes up to **205** and rainfall up to **300**.

If we use a distance-based model like **KNN** (K-Nearest Neighbors), it calculates the distance between two soil samples like this:

```
Distance = sqrt((N1-N2)^2 + (P1-P2)^2 + ... + (pH1-pH2)^2 + (rainfall1-rainfall2)^2)
```

Since Nitrogen and Rainfall have much bigger numbers, they **dominate** the distance calculation. A difference of 50 in Nitrogen will completely overshadow a difference of 2 in pH, even though both differences might be equally important for crop recommendation.

### The Solution: Feature Scaling

We used two scaling techniques to demonstrate the concept:

#### StandardScaler (Z-Score Normalization)

Transforms every feature to have **Mean = 0** and **Standard Deviation = 1**:

```
z = (x - mean) / standard_deviation
```

| Feature | Before (Original) | After (StandardScaler) |
|---------|-------------------|----------------------|
| Nitrogen = 90 | 90 | 0.35 |
| pH = 6.5 | 6.5 | -0.12 |
| Rainfall = 200 | 200 | 0.48 |

Now all features are on the **same scale** centered around 0.

#### MinMaxScaler (Range Normalization)

Transforms every feature to a fixed range of **0 to 1**:

```
x_new = (x - x_min) / (x_max - x_min)
```

| Feature | Before (Original) | After (MinMaxScaler) |
|---------|-------------------|---------------------|
| Nitrogen = 90 | 90 | 0.64 |
| pH = 6.5 | 6.5 | 0.47 |
| Rainfall = 200 | 200 | 0.64 |

### What We Did in the Code

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

numeric_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
X_raw = df_crop[numeric_features]

# Method 1: StandardScaler
std_scaler = StandardScaler()
X_std = pd.DataFrame(std_scaler.fit_transform(X_raw), columns=numeric_features)

# Method 2: MinMaxScaler
minmax_scaler = MinMaxScaler()
X_minmax = pd.DataFrame(minmax_scaler.fit_transform(X_raw), columns=numeric_features)
```

We also generated a **comparison plot** (`feature_scaling_comparison.png`) showing the original Rainfall distribution versus StandardScaler versus MinMaxScaler distributions side-by-side.

### Why is This Important?

- **KNN** measures Euclidean distance — unscaled data makes large-value features dominate.
- **Linear Regression** weight optimization converges faster with scaled data.
- **Decision Trees and Random Forest** are NOT affected by scaling (they split on thresholds, not distances). But it's still best practice to scale.

---

## Step 4: Train-Test Data Splitting

### The Problem

If we train our model on ALL 200 samples and then test it on the SAME 200 samples, it will get ~100% accuracy. But that doesn't mean it actually learned — it just **memorized** the answers. This is like giving a student the exact exam paper to study from, then testing them on the same paper.

### The Solution: 80/20 Train-Test Split

We divide the data into two separate parts:
- **Training Set (80% = 160 samples):** The model learns patterns from this data.
- **Testing Set (20% = 40 samples):** The model is evaluated on this data, which it has **never seen** during training.

### What We Did in the Code

```python
from sklearn.model_selection import train_test_split

X = X_std                # Scaled features (after StandardScaler)
y = df_crop['label']     # Target crop labels

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 20% for testing
    random_state=42,     # Fixed seed for reproducible results
    stratify=y           # Keep equal class proportions
)

print(f"Training Set: {X_train.shape[0]} samples")  # 160 samples
print(f"Testing Set:  {X_test.shape[0]} samples")   # 40 samples
```

### What Does `stratify=y` Do?

Without stratification, random splitting might put all `"rice"` samples in training and zero in testing. That would make it impossible to evaluate if the model can predict rice.

**`stratify=y`** ensures that every crop class (rice, maize, chickpea, etc.) appears in the **exact same percentage** in both training and testing sets.

```
Example with stratify=y:
  Full Dataset:  20% rice, 15% maize, 10% chickpea, ...
  Training Set:  20% rice, 15% maize, 10% chickpea, ...  (same ratios!)
  Testing Set:   20% rice, 15% maize, 10% chickpea, ...  (same ratios!)
```

### What Does `random_state=42` Do?

Every time you run `train_test_split`, it randomly shuffles data before splitting. This means you get different results each run. Setting `random_state=42` fixes the randomness so that **every time you run the code, you get the exact same split**. This is important for reproducibility (showing the same results to your professor every time).

### Why is This Important?

- **Prevents data leakage:** Testing on unseen data proves real-world generalization.
- **Detects overfitting:** If training accuracy is 99% but testing accuracy is 50%, the model memorized instead of learning.
- **Reproducibility:** `random_state=42` ensures consistent results across runs.

---

## Complete Data Flow Summary

```
RAW AGRICULTURAL CSV FILES
    |
    | pd.read_csv()
    v
PANDAS DATAFRAMES (df_crop: 200x8, df_fert: 200x9)
    |
    | df.isnull().sum()
    v
STEP 1: INSPECTION (Confirmed 0 missing values)
    |
    | LabelEncoder().fit_transform()
    v
STEP 2: ENCODING ("Clayey" -> 0, "Sandy" -> 4, ...)
    |
    | StandardScaler().fit_transform()
    v
STEP 3: SCALING (N: 0-140 -> Mean=0 Std=1, pH: 3-9 -> Mean=0 Std=1)
    |
    | train_test_split(test_size=0.2, stratify=y)
    v
STEP 4: SPLITTING
    |
    +-- X_train (160 samples) --> Model LEARNS from these
    +-- X_test  (40 samples)  --> Model is TESTED on these
    +-- y_train (160 labels)
    +-- y_test  (40 labels)
```

---

## What I Learned from Tutorial 1 (Write This in Your Notebook)

1. **Data Inspection** is the first step in any ML project. We use `df.shape` to check dimensions and `df.isnull().sum()` to detect missing values. Our agricultural datasets had zero missing values.

2. **Categorical Encoding** is necessary because ML algorithms perform mathematical matrix operations and cannot compute on text strings. We used `LabelEncoder` to map soil types and crop types into integer indices.

3. **Feature Scaling** is critical for distance-based algorithms (KNN) and gradient-based optimizers (Linear Regression). Without scaling, features with large ranges (Nitrogen: 0-140) dominate features with small ranges (pH: 3.5-9.9). `StandardScaler` normalizes all features to Mean=0 and Std=1.

4. **Train-Test Splitting** (80/20 with stratification) ensures we evaluate our model on completely unseen data, preventing overfitting and data leakage. The `stratify=y` parameter guarantees balanced class representation in both sets.
