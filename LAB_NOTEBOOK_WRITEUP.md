# 📓 Machine Learning Lab Notebook Writeup & Learning Outcomes

---

## 📌 EXPERIMENT / TUTORIAL 1 (T1): Data Preprocessing in Python

### **Aim**
To implement data preprocessing techniques in Python, including handling missing values, encoding categorical variables, feature scaling, and train-test data splitting on agricultural datasets.

---

### **Theory & Key Concepts**
1. **Data Preprocessing**: Raw real-world data is often incomplete, inconsistent, and contains noise. Preprocessing converts raw data into a clean format suitable for Machine Learning models.
2. **Categorical Encoding**: ML models only process numerical input. Categorical columns (like `Soil Type` or `Crop Type`) must be encoded into numbers:
   - **Label Encoding**: Assigns a unique integer ($0, 1, 2...$) to each category.
   - **One-Hot Encoding**: Creates binary indicator columns for each category.
3. **Feature Scaling**: Features often have vastly different ranges (e.g., $N$ ranges from $0-140$, while $\text{pH}$ ranges from $3.5-9.0$).
   - **StandardScaler**: Transforms data to have Mean $\mu = 0$ and Variance $\sigma^2 = 1$ ($z = \frac{x - \mu}{\sigma}$).
   - **MinMaxScaler**: Scales data strictly between $0$ and $1$ ($x_{new} = \frac{x - x_{min}}{x_{max} - x_{min}}$).
4. **Train-Test Split**: Splitting data (typically $80\%$ Train, $20\%$ Test) ensures we evaluate our model on unseen data.

---

### **Execution & Output Summary**
- Checked for missing values (`df.isnull().sum()`).
- Encoded categorical features (`Soil Type` & `Crop Type`) using `LabelEncoder`.
- Scaled numerical features ($N, P, K, \text{temperature}, \text{humidity}, \text{pH}, \text{rainfall}$) using `StandardScaler` and `MinMaxScaler`.
- Generated plot `t1_preprocessing_output/feature_scaling_comparison.png`.

---

### **💡 What I Have Learned from T1 (Write this in your Notebook):**
> 1. Raw agricultural soil data cannot be directly fed into machine learning algorithms without preprocessing.
> 2. Algorithms like KNN and Logistic Regression are distance-sensitive; without **StandardScaler**, high-magnitude features (like Potassium or Rainfall) would dominate low-magnitude features (like pH).
> 3. Categorical variables (`Soil Type`, `Crop Type`) must be numericalized via **Label Encoding** so algorithms can perform matrix computations on them.
> 4. Train-test splitting ($80/20$) is essential to prevent data leakage and evaluate real-world generalization.

---

## 📌 EXPERIMENT / TUTORIAL 2 (T2): Linear Regression & Regularization in Python

### **Aim**
To build and evaluate Linear Regression, Ridge ($L_2$), and Lasso ($L_1$) models in Python to predict continuous environmental outcomes (e.g., Rainfall / Soil Moisture).

---

### **Theory & Key Concepts**
1. **Linear Regression**: A parametric supervised learning algorithm that models a linear relationship between input features $X$ and a continuous target $y$:
   $$y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + ... + \beta_n X_n + \epsilon$$
2. **Evaluation Metrics**:
   - **Mean Absolute Error (MAE)**: Average magnitude of errors $\frac{1}{n}\sum |y - \hat{y}|$.
   - **Mean Squared Error (MSE)**: Penalizes larger errors $\frac{1}{n}\sum (y - \hat{y})^2$.
   - **Root Mean Squared Error (RMSE)**: Error in original units $\sqrt{\text{MSE}}$.
   - **$R^2$ Score (Coefficient of Determination)**: Percentage of variance explained ($0.0 \text{ to } 1.0$).
3. **Regularization**: Prevents **Overfitting** by penalizing large feature weights:
   - **Ridge Regression ($L_2$)**: Adds penalty $\lambda \sum \beta_i^2$ (shrinks weights smoothly).
   - **Lasso Regression ($L_1$)**: Adds penalty $\lambda \sum |\beta_i|$ (can shrink irrelevant weights to $0$, performing feature selection).
4. **Bias-Variance Tradeoff**: High bias leads to **underfitting** (too simple); high variance leads to **overfitting** (too complex). Regularization balances this tradeoff.

---

### **Execution & Output Summary**
- Trained Linear Regression, Ridge ($L_2$), and Lasso ($L_1$) models to predict `rainfall`/`Moisture`.
- Evaluated models using MAE, MSE, RMSE, and $R^2$ Score.
- Plotted Actual vs. Predicted values (`t2_regression_output/actual_vs_predicted.png`).
- Compared feature coefficients (`t2_regression_output/coefficients_comparison.png`).

---

### **💡 What I Have Learned from T2 (Write this in your Notebook):**
> 1. **Linear Regression** predicts continuous values by fitting an optimal hyper-plane through feature space.
> 2. Metrics like **$R^2$ score** indicate how well independent variables (temperature, humidity, N, P, K) explain the variance in the target variable.
> 3. Standard Ordinary Least Squares (OLS) Linear Regression is prone to overfitting when features are correlated.
> 4. **Ridge ($L_2$) and Lasso ($L_1$) Regularization** control model complexity by shrinking feature weights, preventing overfitting and balancing the Bias-Variance tradeoff.

---

## 📌 EXPERIMENT / TUTORIAL 3 (T3): Cross-Validation & Learning Curves in Python

### **Aim**
To implement K-Fold Cross-Validation and plot Learning Curves in Python to evaluate model stability, prevent overfitting, and analyze model generalization.

---

### **Theory & Key Concepts**
1. **Cross-Validation**: A single train-test split can be biased depending on which random samples land in test data. **K-Fold Cross-Validation** splits data into $K$ equal subsets (folds):
   - Trains on $K-1$ folds and tests on the remaining $1$ fold.
   - Repeats $K$ times and averages the performance score.
2. **Stratified K-Fold**: Ensures every fold maintains the same percentage of samples for each target class as the complete dataset.
3. **Learning Curve**: A graph comparing **Training Score** vs **Validation Score** over increasing dataset size.
   - **Underfitting (High Bias)**: Both training and validation scores are low.
   - **Overfitting (High Variance)**: Training score is very high ($~100\%$), but validation score remains significantly lower (large gap).
   - **Good Fit**: Both training and validation scores converge to a high performance value with a small gap.

---

### **Execution & Output Summary**
- Executed $5$-Fold and $10$-Fold Stratified Cross-Validation on the classification pipeline.
- Calculated mean cross-validation score and standard deviation (variance across folds).
- Plotted Learning Curves saved in `t3_crossval_output/learning_curve.png`.

---

### **💡 What I Have Learned from T3 (Write this in your Notebook):**
> 1. A single train-test split can give misleading accuracy results depending on how the data was randomly split.
> 2. **K-Fold Cross-Validation** provides a robust, unbiased estimate of how well the model will perform on completely unseen real-world farm data.
> 3. The **Standard Deviation across folds** measures model stability—a low standard deviation means the model generalizes reliably.
> 4. **Learning Curves** visually diagnose model health: a large gap between training and validation scores signifies **overfitting (high variance)**, while low scores on both indicate **underfitting (high bias)**.
