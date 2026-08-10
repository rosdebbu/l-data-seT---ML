# Tutorial 3 (T3): Cross-Validation & Learning Curves in Python — Detailed Guide

## What is This Tutorial About?

In Tutorial 1 (T1), we cleaned and preprocessed our data. In Tutorial 2 (T2), we built Linear Regression models and learned evaluation metrics. Now in Tutorial 3 (T3), we tackle a deeper question:

**"How do we know if our model's accuracy score is actually reliable?"**

When you run `train_test_split` and get 90% accuracy, that number depends on *which* random 20% of data ended up in the test set. If you split differently, you might get 85% or 95%. So which score is real?

**Cross-Validation** solves this by testing the model on every part of the data. **Learning Curves** then visually show us if our model is overfitting or underfitting.

---

## The Problem: Why a Single Train-Test Split Can Be Misleading

### Example of the Problem

Imagine our Crop dataset has 200 samples. We do an 80/20 split:

```
Split A (by random chance):
  Training:  160 samples (happens to include all the "easy" samples)
  Testing:   40 samples  (happens to include mostly "rice" and "maize")
  Accuracy:  95%  (Looks great!)

Split B (different random chance):
  Training:  160 samples (happens to miss some important patterns)
  Testing:   40 samples  (happens to include tricky edge cases)
  Accuracy:  78%  (Looks bad!)
```

Both use the same model on the same data — but the accuracy changes by 17% just because of the random split! Which number should you report to your professor?

**Neither.** You should use **Cross-Validation** to get an average across multiple splits.

---

## Our Setup: What Data and Model We Use

### The Dataset

We use the same **Crop Recommendation** dataset from T1:
- **Features (X):** N, P, K, temperature, humidity, pH, rainfall (7 features)
- **Target (y):** Crop label (rice, maize, chickpea, etc.)
- **Task:** Classification (predicting which crop to grow)

### The Model

We use **Random Forest Classifier** with 50 decision trees:

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=50, random_state=42)
```

**Why Random Forest?** It's robust, handles multiple classes well, and is one of the best general-purpose classification algorithms. It builds 50 individual decision trees and takes a majority vote.

### Preprocessing (Same as T1)

```python
from sklearn.preprocessing import StandardScaler

X = df.drop(columns=['label'])       # All columns except crop name
y = df['label']                       # The crop name we want to predict

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)    # Scale all features to Mean=0, Std=1
```

---

## Step 1: K-Fold Cross-Validation

### What is K-Fold Cross-Validation?

Instead of splitting data into one fixed training and testing set, we divide the entire dataset into **K equal parts** (called "folds"). Then we run K separate experiments:

- **Round 1:** Train on Folds 2, 3, 4, 5 → Test on Fold 1
- **Round 2:** Train on Folds 1, 3, 4, 5 → Test on Fold 2
- **Round 3:** Train on Folds 1, 2, 4, 5 → Test on Fold 3
- **Round 4:** Train on Folds 1, 2, 3, 5 → Test on Fold 4
- **Round 5:** Train on Folds 1, 2, 3, 4 → Test on Fold 5

### Visual Diagram (5-Fold)

```
Round 1:  [TEST ] [TRAIN] [TRAIN] [TRAIN] [TRAIN]  --> Accuracy = 92%
Round 2:  [TRAIN] [TEST ] [TRAIN] [TRAIN] [TRAIN]  --> Accuracy = 88%
Round 3:  [TRAIN] [TRAIN] [TEST ] [TRAIN] [TRAIN]  --> Accuracy = 95%
Round 4:  [TRAIN] [TRAIN] [TRAIN] [TEST ] [TRAIN]  --> Accuracy = 90%
Round 5:  [TRAIN] [TRAIN] [TRAIN] [TRAIN] [TEST ]  --> Accuracy = 93%

Mean Accuracy = (92 + 88 + 95 + 90 + 93) / 5 = 91.6%
Standard Deviation = 2.3%
```

**Every single data sample gets tested exactly once.** No sample is left untested and no sample appears in the test set twice.

### What is Stratified K-Fold? (What We Actually Use)

Normal K-Fold splits data randomly. But what if, by random chance, one fold ends up with zero "rice" samples? Then the model can't be tested on rice for that round.

**Stratified K-Fold** guarantees that every fold has the **same percentage of each crop class** as the full dataset:

```
Full dataset:   20% rice, 15% maize, 10% chickpea, ...

Fold 1:         20% rice, 15% maize, 10% chickpea, ...  (same!)
Fold 2:         20% rice, 15% maize, 10% chickpea, ...  (same!)
Fold 3:         20% rice, 15% maize, 10% chickpea, ...  (same!)
Fold 4:         20% rice, 15% maize, 10% chickpea, ...  (same!)
Fold 5:         20% rice, 15% maize, 10% chickpea, ...  (same!)
```

### What We Did in the Code

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score

model = RandomForestClassifier(n_estimators=50, random_state=42)

# Run 5-Fold and 10-Fold Cross-Validation
for k in [5, 10]:
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_scaled, y, cv=skf, scoring='accuracy')

    print(f"Scores for each fold: {np.round(scores, 4)}")
    print(f"Mean Accuracy: {scores.mean():.4f}")
    print(f"Standard Deviation: {scores.std():.4f}")
```

### Understanding the Two Parameters

**`n_splits=k`:** How many folds to create (5 or 10).

**`shuffle=True`:** Randomly shuffle the data before splitting into folds. Without shuffling, if the CSV file is sorted by crop name, the first fold would contain only one crop.

### Understanding the Output

```
5-Fold Stratified Cross Validation Results:
  Scores for each fold: [0.925  0.875  0.950  0.900  0.925]
  Mean Accuracy: 0.9150 (91.50%)
  Standard Deviation: 0.0245

10-Fold Stratified Cross Validation Results:
  Scores for each fold: [0.90  0.95  0.85  0.90  0.95  0.90  0.85  0.95  0.90  0.95]
  Mean Accuracy: 0.9100 (91.00%)
  Standard Deviation: 0.0374
```

### How to Read This

- **Mean Accuracy = 91.50%:** This is our model's **true estimated performance** — much more trustworthy than any single train-test split.
- **Standard Deviation = 0.0245 (2.45%):** This tells us how much accuracy **varies** across folds:
  - **Low StdDev (< 3%):** Model is **stable** — it performs consistently on different data subsets. Good sign!
  - **High StdDev (> 5%):** Model is **unstable** — performance depends heavily on which data it sees. Might indicate overfitting or insufficient data.

### 5-Fold vs 10-Fold: Which is Better?

| | 5-Fold | 10-Fold |
|---|---|---|
| **Training set size per fold** | 80% of data | 90% of data |
| **Test set size per fold** | 20% of data | 10% of data |
| **Computation time** | Faster (5 rounds) | Slower (10 rounds) |
| **Bias** | Slightly higher (less training data per round) | Lower (more training data per round) |
| **Variance** | Lower (larger test sets = more stable scores) | Higher (smaller test sets = more noisy scores) |
| **Most common choice** | Default for most projects | When you have small datasets |

---

## Step 2: Learning Curves — Diagnosing Overfitting vs Underfitting

### What is a Learning Curve?

A Learning Curve is a plot that answers the question: **"If I give my model more and more training data, how does its performance change?"**

We start by training the model on only 10% of the data, then 20%, 30%, all the way up to 100%. At each step, we record two scores:
- **Training Score:** How accurate is the model on the data it learned from?
- **Validation Score:** How accurate is the model on data it hasn't seen? (measured via cross-validation)

### What We Did in the Code

```python
from sklearn.model_selection import learning_curve

train_sizes, train_scores, val_scores = learning_curve(
    estimator=model,         # Our Random Forest model
    X=X_scaled,              # Scaled features
    y=y,                     # Target crop labels
    train_sizes=np.linspace(0.1, 1.0, 10),  # 10%, 20%, ... 100%
    cv=5,                    # 5-fold cross-validation at each step
    scoring='accuracy',      # Measure accuracy
    n_jobs=-1                # Use all CPU cores for speed
)
```

### What Each Parameter Does

| Parameter | Value | What it Does |
|-----------|-------|-------------|
| `estimator` | `model` | The ML model to evaluate (Random Forest) |
| `train_sizes` | `np.linspace(0.1, 1.0, 10)` | 10 steps from 10% to 100% of training data |
| `cv=5` | 5 | At each step, use 5-fold cross-validation to get a reliable score |
| `scoring='accuracy'` | accuracy | The metric to measure |
| `n_jobs=-1` | -1 | Use all available CPU cores to speed up computation |

### How We Plot It

```python
train_mean = np.mean(train_scores, axis=1)   # Average training score across 5 folds
val_mean   = np.mean(val_scores, axis=1)     # Average validation score across 5 folds
train_std  = np.std(train_scores, axis=1)    # Spread of training scores
val_std    = np.std(val_scores, axis=1)      # Spread of validation scores

# Plot the two lines
ax.plot(train_sizes, train_mean, 'o-', color='blue', label='Training Score')
ax.plot(train_sizes, val_mean, 's-', color='green', label='Validation Score')

# Add shaded confidence bands (Mean +/- Std)
ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.15)
ax.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.15)
```

The **shaded bands** show the range of scores across the 5 folds — wider bands mean less stable scores.

### How to Read the Learning Curve Plot

The plot has two lines:
- **Blue line (Training Score):** How well the model fits its own training data.
- **Green line (Validation Score):** How well the model predicts unseen data.

There are **3 possible scenarios**:

---

### Scenario 1: GOOD FIT (What We Want!)

```
Score
 1.0  ═══════════════════════════  <-- Training Score (high)
      \
 0.9   ──────────────────────────  <-- Validation Score (close & high)
      
 0.0  ───┬───┬───┬───┬───┬───┬──
      10% 20% 30% 50% 70% 100%
```

- Both lines are **high** (good accuracy).
- Both lines are **close together** (small gap).
- **Conclusion:** The model learned real patterns and generalizes well.
- **Action:** No fix needed! Model is ready.

---

### Scenario 2: OVERFITTING (High Variance)

```
Score
 1.0  ═══════════════════════════  <-- Training Score (perfect 100%)
      
 0.6   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  <-- Validation Score (much lower)
       ↑                      ↑
       |______ BIG GAP ______|
 0.0  ───┬───┬───┬───┬───┬───┬──
      10% 20% 30% 50% 70% 100%
```

- Training Score is **very high** (~100%).
- Validation Score is **much lower** (big gap between the lines).
- **Conclusion:** The model memorized training data (including noise) instead of learning real patterns. It fails on new data.
- **How to Fix:**
  1. Add **more training data** (more soil samples).
  2. **Simplify the model** (reduce number of trees, limit tree depth).
  3. Apply **Regularization** (like Ridge/Lasso from T2).

---

### Scenario 3: UNDERFITTING (High Bias)

```
Score
 1.0
      
 0.5  ═══════════════════════════  <-- Training Score (low)
 0.4  ──────────────────────────  <-- Validation Score (also low)
      
 0.0  ───┬───┬───┬───┬───┬───┬──
      10% 20% 30% 50% 70% 100%
```

- Training Score is **low** (model can't even fit training data).
- Validation Score is **also low** (and close to training score).
- **Conclusion:** The model is too simple to capture the patterns in the data.
- **How to Fix:**
  1. Use a **more complex model** (switch from Logistic Regression to Random Forest).
  2. Add **more features** (include more soil/climate variables).
  3. **Reduce regularization** (lower the lambda value).

---

## How T1, T2, and T3 Connect Together

All three tutorials build on each other in a logical pipeline:

```
T1: DATA PREPROCESSING
    |
    | "Can the model even read this data?"
    | Clean it, encode text, scale numbers, split into train/test
    v
T2: LINEAR REGRESSION & REGULARIZATION
    |
    | "Can we build a model and evaluate it?"
    | Fit regression, measure MAE/RMSE/R2, apply Ridge & Lasso
    v
T3: CROSS-VALIDATION & LEARNING CURVES
    |
    | "Can we TRUST the model's accuracy score?"
    | Test across K folds, measure stability, diagnose overfit/underfit
    v
RELIABLE, VALIDATED MODEL READY FOR DEPLOYMENT
```

---

## Complete Data Flow Summary

```
CROP RECOMMENDATION CSV (200 rows x 8 columns)
    |
    | Load with pd.read_csv(), separate features and target
    v
X (200 x 7 features)  +  y (200 crop labels)
    |
    | StandardScaler().fit_transform()
    v
X_scaled (200 x 7 normalized features)
    |
    +--[ STEP 1: Cross-Validation ]
    |     |
    |     | StratifiedKFold(n_splits=5)
    |     v
    |   Round 1: Train on Folds 2-5, Test on Fold 1 --> Score 1
    |   Round 2: Train on Folds 1,3-5, Test on Fold 2 --> Score 2
    |   Round 3: Train on Folds 1-2,4-5, Test on Fold 3 --> Score 3
    |   Round 4: Train on Folds 1-3,5, Test on Fold 4 --> Score 4
    |   Round 5: Train on Folds 1-4, Test on Fold 5 --> Score 5
    |     |
    |     v
    |   Mean Accuracy = average(Score1..Score5)
    |   Standard Deviation = std(Score1..Score5)
    |
    +--[ STEP 2: Learning Curve ]
          |
          | Train on 10%, 20%, 30%, ... 100% of data
          | At each size, compute Training Score & Validation Score
          v
        PLOT:
          Blue line  = Training Score over sample sizes
          Green line = Validation Score over sample sizes
          Gap between lines = Overfitting indicator
```

---

## Key Terms Summary Table

| Term | Simple Definition |
|------|------------------|
| **K-Fold CV** | Split data into K parts, train on K-1, test on 1, repeat K times |
| **Stratified** | Each fold keeps the exact same class ratio as the full dataset |
| **Mean Accuracy** | Average score across all K rounds — the "true" model performance |
| **Standard Deviation** | How much scores vary across folds — measures model stability |
| **Learning Curve** | Plot of Training Score vs Validation Score over increasing data sizes |
| **Overfitting** | Model memorizes training data, fails on new data (High Variance) |
| **Underfitting** | Model is too simple to learn any patterns (High Bias) |
| **Training Score** | Accuracy on data the model was trained on |
| **Validation Score** | Accuracy on unseen data (via cross-validation) |
| **n_jobs=-1** | Use all CPU cores to speed up computation |

---

## What I Learned from Tutorial 3 (Write This in Your Notebook)

1. **Single train-test splits are unreliable** because accuracy depends on which random subset of data ends up in the test set. Different splits can give drastically different accuracy scores (e.g. 78% vs 95%) for the same model.

2. **K-Fold Cross-Validation** divides the dataset into K equal folds and runs K separate train-test experiments, ensuring every data sample gets tested exactly once. The mean accuracy across all folds gives a robust, unbiased estimate of model performance.

3. **Stratified K-Fold** is preferred over standard K-Fold for classification tasks because it preserves the exact class distribution (ratio of rice, maize, chickpea, etc.) in every fold, preventing biased evaluation on imbalanced datasets.

4. **Standard Deviation across folds** measures model stability. A low standard deviation (below 3%) indicates the model performs consistently regardless of data partitioning. A high standard deviation suggests the model may be overfitting or the dataset may be too small.

5. **Learning Curves** visualize how Training Score and Validation Score change as training data size increases. A large gap between the two lines indicates **Overfitting (High Variance)**, while both lines remaining low indicates **Underfitting (High Bias)**. A good model shows both lines converging at a high score.
