# ============================================================
# Tutorial 1 (T1): Data Preprocessing in Python
# ============================================================
# Goal: Learn data cleaning, missing value handling, categorical
# encoding, feature scaling, and train-test data splitting.
# Compatible with local Python & Google Colab.
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder

# --------------------------------------------------
# Setup output directory
# --------------------------------------------------
OUT_DIR = "t1_preprocessing_output"
os.makedirs(OUT_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")

# Ensure dataset directory exists
os.makedirs("data", exist_ok=True)
crop_csv = os.path.join("data", "Crop_recommendation.csv")
fert_csv = os.path.join("data", "Fertilizer_Prediction.csv")

# Create demo datasets automatically if running on Google Colab or empty directory
if not os.path.exists(crop_csv):
    print("[INFO] Creating demo Crop_recommendation.csv...")
    crops = ["rice", "maize", "chickpea", "kidneybeans", "pigeonpeas", "mothbeans", "mungbean", "blackgram", "lentil", "pomegranate"]
    df_c = pd.DataFrame({
        'N': np.random.randint(10, 140, 200),
        'P': np.random.randint(5, 145, 200),
        'K': np.random.randint(15, 205, 200),
        'temperature': np.random.uniform(8.0, 43.0, 200),
        'humidity': np.random.uniform(14.0, 100.0, 200),
        'ph': np.random.uniform(3.5, 9.9, 200),
        'rainfall': np.random.uniform(20.0, 300.0, 200),
        'label': np.random.choice(crops, 200)
    })
    df_c.to_csv(crop_csv, index=False)

if not os.path.exists(fert_csv):
    print("[INFO] Creating demo Fertilizer_Prediction.csv...")
    ferts = ["Urea", "DAP", "14-35-14", "28-28", "17-17-17", "20-20", "10-26-26"]
    soils = ["Clayey", "Sandy", "Loamy", "Black", "Red"]
    crop_types = ["Maize", "Sugarcane", "Cotton", "Tobacco", "Paddy", "Barley", "Wheat", "Millets"]
    df_f = pd.DataFrame({
        'Temperature': np.random.randint(25, 40, 200),
        'Humidity': np.random.randint(50, 75, 200),
        'Moisture': np.random.randint(25, 70, 200),
        'Soil Type': np.random.choice(soils, 200),
        'Crop Type': np.random.choice(crop_types, 200),
        'Nitrogen': np.random.randint(0, 45, 200),
        'Phosphorous': np.random.randint(0, 45, 200),
        'Potassium': np.random.randint(0, 45, 200),
        'Fertilizer Name': np.random.choice(ferts, 200)
    })
    df_f.to_csv(fert_csv, index=False)

print("=" * 60)
print("TUTORIAL 1 (T1): DATA PREPROCESSING PIPELINE")
print("=" * 60)

# Load datasets
df_crop = pd.read_csv(crop_csv)
df_fert = pd.read_csv(fert_csv)

# --------------------------------------------------
# Step 1: Inspection & Data Cleaning
# --------------------------------------------------
print("\n[Step 1] Inspecting Crop & Fertilizer Datasets")
print(f"  Crop Dataset Shape:       {df_crop.shape}")
print(f"  Fertilizer Dataset Shape: {df_fert.shape}")

print("\nMissing values in Crop Dataset:")
print(df_crop.isnull().sum())

print("\nMissing values in Fertilizer Dataset:")
print(df_fert.isnull().sum())

# --------------------------------------------------
# Step 2: Categorical Encoding
# --------------------------------------------------
print("\n[Step 2] Categorical Encoding with LabelEncoder")
df_fert_processed = df_fert.copy()

le_soil = LabelEncoder()
le_crop = LabelEncoder()
le_fert = LabelEncoder()

df_fert_processed['Soil Type_encoded'] = le_soil.fit_transform(df_fert_processed['Soil Type'])
df_fert_processed['Crop Type_encoded'] = le_crop.fit_transform(df_fert_processed['Crop Type'])
df_fert_processed['Fertilizer_encoded'] = le_fert.fit_transform(df_fert_processed['Fertilizer Name'])

print(f"  [OK] Encoded Soil Type:   {dict(zip(le_soil.classes_[:3], le_soil.transform(le_soil.classes_[:3])))}...")
print(f"  [OK] Encoded Crop Type:   {dict(zip(le_crop.classes_[:3], le_crop.transform(le_crop.classes_[:3])))}...")
print(f"  [OK] Encoded Fertilizer:  {dict(zip(le_fert.classes_[:3], le_fert.transform(le_fert.classes_[:3])))}...")

# --------------------------------------------------
# Step 3: Feature Scaling (StandardScaler vs MinMaxScaler)
# --------------------------------------------------
print("\n[Step 3] Feature Scaling (StandardScaler vs MinMaxScaler)")
numeric_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
X_raw = df_crop[numeric_features]

std_scaler = StandardScaler()
X_std = pd.DataFrame(std_scaler.fit_transform(X_raw), columns=numeric_features)

minmax_scaler = MinMaxScaler()
X_minmax = pd.DataFrame(minmax_scaler.fit_transform(X_raw), columns=numeric_features)

# Save comparison plot
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.histplot(X_raw['rainfall'], ax=axes[0], color='skyblue', kde=True)
axes[0].set_title("Original Rainfall Distribution")

sns.histplot(X_std['rainfall'], ax=axes[1], color='salmon', kde=True)
axes[1].set_title("StandardScaler (Mean=0, Std=1)")

sns.histplot(X_minmax['rainfall'], ax=axes[2], color='lightgreen', kde=True)
axes[2].set_title("MinMaxScaler (Range 0 to 1)")

plt.tight_layout()
plot_path = os.path.join(OUT_DIR, "feature_scaling_comparison.png")
plt.savefig(plot_path)
plt.close()
print(f"  [OK] Saved plot: {plot_path}")

# --------------------------------------------------
# Step 4: Train / Test Data Splitting
# --------------------------------------------------
print("\n[Step 4] Train-Test Splitting (80% Train, 20% Test)")
X = X_std
y = df_crop['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"  Training Set (80%): {X_train.shape[0]} samples")
print(f"  Testing Set  (20%): {X_test.shape[0]} samples")
print(f"  Feature Count:       {X_train.shape[1]}")

print("\n" + "=" * 60)
print("TUTORIAL 1 (T1) COMPLETED SUCCESSFULLY!")
print("=" * 60)
