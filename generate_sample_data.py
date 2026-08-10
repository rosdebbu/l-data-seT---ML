# ============================================================
# Generate Demo Sample Datasets (for instant testing)
# ============================================================
import os
import numpy as np
import pandas as pd

os.makedirs("data", exist_ok=True)

# 1. Sample Crop Recommendation Data
crops = ["rice", "maize", "chickpea", "kidneybeans", "pigeonpeas", "mothbeans", "mungbean", "blackgram", "lentil", "pomegranate"]
n_samples = 200

crop_df = pd.DataFrame({
    "N": np.random.randint(10, 140, n_samples),
    "P": np.random.randint(5, 145, n_samples),
    "K": np.random.randint(15, 205, n_samples),
    "temperature": np.random.uniform(8.0, 43.0, n_samples),
    "humidity": np.random.uniform(14.0, 100.0, n_samples),
    "ph": np.random.uniform(3.5, 9.9, n_samples),
    "rainfall": np.random.uniform(20.0, 300.0, n_samples),
    "label": np.random.choice(crops, n_samples)
})
crop_path = os.path.join("data", "Crop_recommendation.csv")
crop_df.to_csv(crop_path, index=False)
print(f"[OK] Generated sample dataset: {crop_path}")

# 2. Sample Fertilizer Prediction Data
fertilizers = ["Urea", "DAP", "14-35-14", "28-28", "17-17-17", "20-20", "10-26-26"]
soils = ["Clayey", "Sandy", "Loamy", "Black", "Red"]
crop_types = ["Maize", "Sugarcane", "Cotton", "Tobacco", "Paddy", "Barley", "Wheat", "Millets"]

fert_df = pd.DataFrame({
    "Temperature": np.random.randint(25, 40, n_samples),
    "Humidity": np.random.randint(50, 75, n_samples),
    "Moisture": np.random.randint(25, 70, n_samples),
    "Soil Type": np.random.choice(soils, n_samples),
    "Crop Type": np.random.choice(crop_types, n_samples),
    "Nitrogen": np.random.randint(0, 45, n_samples),
    "Phosphorous": np.random.randint(0, 45, n_samples),
    "Potassium": np.random.randint(0, 45, n_samples),
    "Fertilizer Name": np.random.choice(fertilizers, n_samples)
})
fert_path = os.path.join("data", "Fertilizer_Prediction.csv")
fert_df.to_csv(fert_path, index=False)
print(f"[OK] Generated sample dataset: {fert_path}")
