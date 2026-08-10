can# Unit 1: Introduction and Types of Learning — Exam Study Guide

> Short, simple, and easy to memorize. Read this before your test and you'll be confident on every topic.

---

## 1. Machine Learning: What & Why?

**What is ML?** Teaching computers to learn patterns from data and make predictions WITHOUT writing explicit rules.

**Normal Programming vs ML:**

| Normal Programming | Machine Learning |
|---|---|
| You write IF-ELSE rules | Computer discovers rules from data |
| Input + Rules = Output | Input + Output = Rules (learned) |
| Breaks when new situations arise | Adapts to new patterns automatically |

**Why do we need ML?**
- Too many variables for manual rules (22 crops, 7 soil features = impossible to write all rules by hand)
- Data is growing faster than humans can analyze it
- Patterns are too complex for human observation (detecting cancer from X-rays)

---

## 2. Examples of ML Applications

| Domain | Application | ML Does What |
|---|---|---|
| Agriculture | Crop Recommendation | Predicts best crop from soil data |
| Healthcare | Disease Detection | Finds tumors in X-ray images |
| Finance | Fraud Detection | Flags suspicious bank transactions |
| Email | Spam Filter | Classifies emails as spam / not spam |
| Shopping | Product Recommendations | "You might also like..." |
| Transport | Self-Driving Cars | Recognizes traffic signs and pedestrians |
| Voice | Siri / Alexa | Converts speech to text |

---

## 3. Training vs Testing

| Training | Testing |
|---|---|
| Feeding data WITH known answers to the model | Evaluating model on NEW unseen data |
| Model adjusts its weights to learn patterns | Tests if the model actually learned |
| Like studying from a textbook | Like taking the real exam |
| Uses 80% of data | Uses 20% of data |

**Key Rule:** NEVER test on the same data you trained on (that's like memorizing exam answers — not real learning).

---

## 4. Positive and Negative Class

Used in **binary classification** (2 outcomes):

| Term | Meaning | Example |
|---|---|---|
| **Positive Class** | The thing we are looking for | Has disease, Is spam, Crop = Rice |
| **Negative Class** | The default / normal case | No disease, Not spam, Crop ≠ Rice |

**4 Possible Prediction Outcomes:**

| | Actually Positive | Actually Negative |
|---|---|---|
| **Predicted Positive** | **True Positive (TP)** — Correct! | **False Positive (FP)** — False alarm |
| **Predicted Negative** | **False Negative (FN)** — Missed! | **True Negative (TN)** — Correct! |

**Memory trick:** First word = was the prediction right? Second word = what did the model predict.

---

## 5. Cross-Validation

**Problem:** A single 80/20 split gives different accuracy each time depending on random luck.

**Solution:** K-Fold Cross-Validation — split data into K equal parts, rotate testing across all parts.

```
5-Fold Cross-Validation:

Round 1: [TEST ] [TRAIN] [TRAIN] [TRAIN] [TRAIN]  --> 92%
Round 2: [TRAIN] [TEST ] [TRAIN] [TRAIN] [TRAIN]  --> 88%
Round 3: [TRAIN] [TRAIN] [TEST ] [TRAIN] [TRAIN]  --> 95%
Round 4: [TRAIN] [TRAIN] [TRAIN] [TEST ] [TRAIN]  --> 90%
Round 5: [TRAIN] [TRAIN] [TRAIN] [TRAIN] [TEST ]  --> 93%

Final Score = Average = 91.6% (reliable!)
```

**Every data point gets tested exactly once.** No lucky or unlucky splits.

---

## 6. Types of Learning

### 6a. Supervised Learning
- Data has **labels** (known answers)
- Model learns input → output mapping
- Example: Given soil data → predict crop name
- Algorithms: Random Forest, KNN, Linear Regression, Decision Tree

### 6b. Unsupervised Learning
- Data has **NO labels** (no known answers)
- Model finds hidden patterns / groupings on its own
- Example: Grouping farmers by similar soil conditions (clustering)
- Algorithms: K-Means, PCA, DBSCAN

### 6c. Semi-Supervised Learning
- **Mix of labeled + unlabeled data**
- Small portion has labels, large portion doesn't
- Model uses labeled data to guide learning on unlabeled data
- Example: 100 soil samples but only 10 have crop labels

**Quick Comparison (Memorize This Table):**

| | Supervised | Unsupervised | Semi-Supervised |
|---|---|---|---|
| **Labels?** | All labeled | No labels | Some labeled |
| **Goal** | Predict output | Find hidden patterns | Predict using limited labels |
| **Example** | Crop Recommendation | Soil clustering | Partially labeled data |

---

## 7. Curse of Dimensionality

**Dimensions = Number of features (columns).**

Our crop dataset has 7 features = 7 dimensions.

**The Curse:** As features increase, data becomes **sparse** (spread too thin). Distance between points becomes meaningless.

**Simple analogy:**
- Finding your friend in a **line** (1D) → Easy, look left/right
- Finding your friend in a **room** (2D) → Harder, scan the floor
- Finding your friend in a **100-floor building** (3D) → Very hard
- Finding your friend in **100 dimensions** → Nearly impossible

**How to fix:**
1. **Feature Selection** — Remove useless features
2. **PCA** — Compress 100 features into 10 important ones
3. **More Data** — Collect more samples to fill the space

---

## 8. Overfitting and Underfitting

**THE MOST ASKED EXAM TOPIC. Memorize this well!**

### Underfitting (Too Simple)

- Model CANNOT learn patterns in data
- Bad on training data AND bad on test data
- Like a student who didn't study — fails everything
- Cause: Model too simple (straight line for curved data)
- Fix: Use a more complex model, add features

### Overfitting (Too Complex)

- Model MEMORIZES training data including noise
- Great on training data, BAD on test data
- Like a student who memorized exact textbook answers — fails when questions change
- Cause: Model too complex (very deep decision tree)
- Fix: Regularization, more data, simpler model

### Good Fit (Just Right)

- Model learns REAL patterns, ignores noise
- Good on training data AND good on test data

```
                  Training Accuracy    Test Accuracy    Problem
Underfitting:          LOW                LOW           Too simple
Good Fit:              HIGH               HIGH          Perfect!
Overfitting:           VERY HIGH          LOW           Memorized noise
```

---

## 9. Linear Regression

**What:** Predicts a continuous number by fitting a straight line/plane.

**Equation:**
```
y = b0 + b1*X1 + b2*X2 + ... + bn*Xn

y  = predicted value (rainfall)
b0 = intercept (starting point)
b1..bn = weights (importance of each feature)
X1..Xn = input features (N, P, K, temp, humidity, pH)
```

**How it learns:** Adjusts weights to minimize the gap between predicted and actual values (minimizes Mean Squared Error).

**Metrics:**

| Metric | What it Measures |
|---|---|
| **MAE** | Average error in original units |
| **MSE** | Average squared error (penalizes big errors) |
| **RMSE** | Square root of MSE (error in original units) |
| **R2** | % of variance explained (0 to 1, higher = better) |

---

## 10. Bias and Variance Tradeoff

**Bias** = Error from making model TOO SIMPLE → Underfitting

**Variance** = Error from making model TOO SENSITIVE to training data → Overfitting

```
Total Error = Bias^2 + Variance + Noise

- Decrease Bias   --> Variance increases
- Decrease Variance --> Bias increases
- You must find the SWEET SPOT in the middle
```

**Dartboard analogy:**

```
High Bias, Low Variance    Low Bias, High Variance    Low Bias, Low Variance
(Always wrong, consistent) (Scattered around target)  (Accurate & consistent)
                                                       = GOAL!
     * * *                       *                         *
    * * * *                   *     *                     * *
     * * *                      *   *                      *
```

---

## 11. Regularization

**What:** Adds a penalty for large weights to PREVENT OVERFITTING.

**Two Types:**

| | Ridge (L2) | Lasso (L1) |
|---|---|---|
| **Penalty** | lambda * sum(weights^2) | lambda * sum(\|weights\|) |
| **Effect** | Shrinks ALL weights toward 0 | Shrinks SOME weights to EXACTLY 0 |
| **Feature Selection** | No (keeps all features) | Yes (drops useless features) |

**Lambda (strength):**
- Lambda = 0 → No regularization (normal model)
- Lambda = small → Light regularization
- Lambda = large → Heavy regularization (all weights → 0 = underfitting)

---

## 12. Learning Curve

A plot of **Training Score** and **Validation Score** over increasing training data sizes.

**How to read it:**

```
Good Fit:     Both lines HIGH and CLOSE together
Overfitting:  Training HIGH, Validation LOW (BIG GAP)
Underfitting: BOTH lines LOW
```

**Fixes:**
- Overfitting → More data, simpler model, regularization
- Underfitting → More complex model, more features

---

## 13. Classification

**What:** Predicting a discrete category (not a number).

| Input Features | Task | Output |
|---|---|---|
| N, P, K, temp, humidity, pH, rainfall | Crop Recommendation | "Rice" or "Maize" |
| Temp, Humidity, Soil Type | Fertilizer Prediction | "Urea" or "DAP" |

**Common Classification Algorithms:**

| Algorithm | How it Works (Simple) |
|---|---|
| **Random Forest** | 100 decision trees vote; majority wins |
| **Decision Tree** | Asks yes/no questions like a flowchart |
| **KNN** | Looks at K nearest neighbors, picks most common class |

**Classification Metrics:**

| Metric | What it Measures |
|---|---|
| **Accuracy** | % of correct predictions out of total |
| **Precision** | Out of predicted positives, how many were actually positive? |
| **Recall** | Out of actual positives, how many did we catch? |
| **F1-Score** | Balance of Precision and Recall |

---

## 14. Error and Noise

**Noise** = Random, meaningless variations that don't represent real patterns.
- Caused by: faulty sensors, typos, natural variability
- Example: pH sensor reads 15.0 (impossible — pH range is 0-14)
- **Cannot be reduced** — it is irreducible error

**Total Error Breakdown:**
```
Total Error = Bias^2 + Variance + Irreducible Noise
                |          |           |
            Too simple  Too complex  Random junk
            (fixable)   (fixable)    (NOT fixable)
```

---

## 15. Parametric vs Non-Parametric Models

| | Parametric | Non-Parametric |
|---|---|---|
| **Assumes** | Fixed mathematical form | No assumption about data shape |
| **Parameters** | Fixed number (doesn't change with data size) | Grows with data size |
| **Speed** | Fast | Slower |
| **Risk** | Underfitting (too rigid) | Overfitting (too flexible) |
| **Examples** | Linear Regression, Logistic Regression | KNN, Decision Tree, Random Forest |

**Parametric = straight ruler** (fixed shape, only angle adjusts)
**Non-Parametric = flexible wire** (bends to fit every point)

---

## 16. Linear Algebra for Machine Learning

**Why it matters:** ALL ML computations use matrices and vectors.

### Vectors
One data sample = one vector:
```
Sample = [N=90, P=42, K=43, Temp=20, Humidity=82, pH=6.5, Rainfall=202]
         (7 numbers = 7-dimensional vector)
```

### Matrices
Entire dataset = a matrix:
```
         N    P    K   Temp  Humidity  pH   Rainfall
Row 1:  [90,  42,  43,  20,    82,   6.5,   202]
Row 2:  [20,  27,  48,  27,    50,   7.0,    65]
Row 3:  [85,  58,  41,  24,    80,   7.1,   150]
= 200 x 7 matrix (200 rows, 7 columns)
```

### Key Operations

| Operation | What it Does | Used For |
|---|---|---|
| **Dot Product** | Multiply elements & sum | Making predictions (X . W) |
| **Transpose** | Flip rows ↔ columns | Matrix algebra formulas |
| **Inverse** | "Undo" a matrix | Solving linear regression weights |
| **Matrix Multiplication** | Combine two matrices | Forward pass in all ML models |

### Prediction Formula
```
Prediction = X * W + b

X = feature matrix (200 x 7)
W = weight vector (7 x 1) — learned by model
b = bias/intercept
```

This single matrix multiplication predicts all 200 outputs at once!

---

## Quick Revision — All 16 Topics in One Line Each

| # | Topic | One-Line Definition |
|---|---|---|
| 1 | Machine Learning | Computers learning patterns from data to make predictions |
| 2 | ML Applications | Spam filter, crop prediction, disease detection, self-driving cars |
| 3 | Training vs Testing | Training = learning from data; Testing = evaluating on unseen data |
| 4 | Positive/Negative Class | Target outcome vs default outcome in binary classification |
| 5 | Cross-Validation | Testing model on K different splits for reliable accuracy |
| 6 | Supervised Learning | Learning from labeled data (input + known answer) |
| 7 | Unsupervised Learning | Finding hidden patterns in unlabeled data |
| 8 | Semi-Supervised | Learning from mix of labeled + unlabeled data |
| 9 | Curse of Dimensionality | More features = sparser data = worse performance |
| 10 | Overfitting | Memorizes training data, fails on new data |
| 11 | Underfitting | Too simple, fails on all data |
| 12 | Linear Regression | Predicting continuous values by fitting a line |
| 13 | Bias-Variance | Too simple = high bias; Too complex = high variance |
| 14 | Regularization | Penalizing large weights to prevent overfitting |
| 15 | Learning Curve | Plot showing training vs validation score over data sizes |
| 16 | Classification | Predicting discrete categories (Rice, Wheat, Urea) |
| 17 | Error & Noise | Total Error = Bias^2 + Variance + Irreducible Noise |
| 18 | Parametric | Fixed-form model (Linear Regression) |
| 19 | Non-Parametric | Flexible model that grows with data (KNN, Decision Tree) |
| 20 | Linear Algebra | Matrix/vector math powering all ML computations |
