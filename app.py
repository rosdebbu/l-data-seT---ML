"""
Crop & Fertilizer ML - Unified Prediction Platform
Backend server powered by FastAPI, scikit-learn, and pandas.
Provides real-time multi-model predictions, dataset introspection,
model benchmarking, and scientific evaluation endpoints.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ============================================================
# APP INITIALIZATION
# ============================================================
app = FastAPI(
    title="Crop & Fertilizer ML",
    description="Machine Learning Prediction System for Crop & Fertilizer Datasets",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_DIR = os.path.join(BASE_DIR, "data")
CHARTS_CROP_DIR = os.path.join(BASE_DIR, "output_charts")
CHARTS_FERT_DIR = os.path.join(BASE_DIR, "output_charts_fertilizer")

try:
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
except Exception as e:
    pass

# ============================================================
# ML MODEL STORAGE & TRAINING
# ============================================================
crop_store = {}
fert_store = {}

def train_crop_models():
    crop_csv = os.path.join(DATA_DIR, "Crop_recommendation.csv")
    if not os.path.exists(crop_csv):
        raise FileNotFoundError(f"Crop dataset not found at {crop_csv}")
    
    df = pd.read_csv(crop_csv)
    features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    target = "label"
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5)
    }
    
    trained_models = {}
    metrics = {}
    
    for name, m in models.items():
        m.fit(X_train_scaled, y_train)
        y_pred = m.predict(X_test_scaled)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        
        trained_models[name] = m
        metrics[name] = {
            "accuracy": round(float(acc) * 100, 2),
            "precision": round(float(prec) * 100, 2),
            "recall": round(float(rec) * 100, 2),
            "f1_score": round(float(f1) * 100, 2)
        }
        
    crop_store["df"] = df
    crop_store["features"] = features
    crop_store["classes"] = sorted(y.unique().tolist())
    crop_store["scaler"] = scaler
    crop_store["models"] = trained_models
    crop_store["metrics"] = metrics
    crop_store["feature_ranges"] = {
        col: {"min": float(df[col].min()), "max": float(df[col].max()), "mean": float(df[col].mean())}
        for col in features
    }
    print("[OK] Crop recommendation models trained successfully.")

def train_fertilizer_models():
    fert_csv = os.path.join(DATA_DIR, "Fertilizer_Prediction.csv")
    if not os.path.exists(fert_csv):
        raise FileNotFoundError(f"Fertilizer dataset not found at {fert_csv}")
        
    df = pd.read_csv(fert_csv)
    target_col = "Fertilizer Name"
    
    le_soil = LabelEncoder()
    le_crop = LabelEncoder()
    
    df["Soil_Type_encoded"] = le_soil.fit_transform(df["Soil Type"])
    df["Crop_Type_encoded"] = le_crop.fit_transform(df["Crop Type"])
    
    feature_cols = [
        "Temperature", "Humidity", "Moisture",
        "Soil_Type_encoded", "Crop_Type_encoded",
        "Nitrogen", "Phosphorous", "Potassium"
    ]
    
    X = df[feature_cols]
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5)
    }
    
    trained_models = {}
    metrics = {}
    
    for name, m in models.items():
        m.fit(X_train_scaled, y_train)
        y_pred = m.predict(X_test_scaled)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        
        trained_models[name] = m
        metrics[name] = {
            "accuracy": round(float(acc) * 100, 2),
            "precision": round(float(prec) * 100, 2),
            "recall": round(float(rec) * 100, 2),
            "f1_score": round(float(f1) * 100, 2)
        }
        
    fert_store["df"] = df
    fert_store["feature_cols"] = feature_cols
    fert_store["le_soil"] = le_soil
    fert_store["le_crop"] = le_crop
    fert_store["soil_types"] = sorted(df["Soil Type"].unique().tolist())
    fert_store["crop_types"] = sorted(df["Crop Type"].unique().tolist())
    fert_store["classes"] = sorted(y.unique().tolist())
    fert_store["scaler"] = scaler
    fert_store["models"] = trained_models
    fert_store["metrics"] = metrics
    print("[OK] Fertilizer prediction models trained successfully.")

# Train models on import/startup
train_crop_models()
train_fertilizer_models()

# ============================================================
# CROP METADATA & ADVICE DICTIONARY
# ============================================================
CROP_METADATA = {
    "rice": {
        "title": "Rice (Oryza sativa)",
        "icon": "🌾",
        "category": "Kharif Cereal",
        "description": "Thrives in high rainfall, heavy clayey soils, and warm humid climates.",
        "growing_season": "June - November (Monsoon)",
        "ideal_conditions": "High N (60-90), Rainfall >180mm, High humidity (80%+), pH 5.5-7.0",
        "economic_value": "Primary staple crop in Asia, high commercial and subsistence value."
    },
    "maize": {
        "title": "Maize / Corn (Zea mays)",
        "icon": "🌽",
        "category": "Coarse Grain / Cereal",
        "description": "Requires well-drained loamy soils, moderate nitrogen, and moderate temperature.",
        "growing_season": "June - September / Year-round",
        "ideal_conditions": "Balanced NPK (70:40:20), Temp 20-27°C, Moderate rainfall (60-100mm)",
        "economic_value": "High demand in food, livestock feed, starch, and biofuel."
    },
    "chickpea": {
        "title": "Chickpea / Bengal Gram (Cicer arietinum)",
        "icon": "🌱",
        "category": "Rabi Pulse / Legume",
        "description": "Nitrogen-fixing legume adapted to cool dry climates and neutral to alkaline soils.",
        "growing_season": "October - March (Winter)",
        "ideal_conditions": "Low N demand (fixes N2), Low rainfall (60-80mm), Neutral pH (6.5-7.5)",
        "economic_value": "Key source of dietary plant protein with high domestic demand."
    },
    "kidneybeans": {
        "title": "Kidney Beans / Rajma (Phaseolus vulgaris)",
        "icon": "🫘",
        "category": "Pulse / Legume",
        "description": "Requires rich humus soil, cool temperature, and high potassium and phosphorus.",
        "growing_season": "February - May / Mid-elevation",
        "ideal_conditions": "High P & K, Moderate Temp (18-24°C), Moderate rainfall (100-150mm)",
        "economic_value": "High market price per quintal, prized pulse crop."
    },
    "pigeonpeas": {
        "title": "Pigeonpeas / Arhar / Tur (Cajanus cajan)",
        "icon": "🌿",
        "category": "Deep-rooted Pulse",
        "description": "Drought-tolerant, deep tap-rooted legume that thrives in semiarid climates.",
        "growing_season": "July - January (6-8 months)",
        "ideal_conditions": "Deep soil, low humidity tolerance, moderate rainfall (90-150mm)",
        "economic_value": "Major pulse in India, commands premium pricing in wholesale markets."
    },
    "mothbeans": {
        "title": "Moth Beans (Vigna aconitifolia)",
        "icon": "🍂",
        "category": "Arid Pulse",
        "description": "Extremely drought-resistant crop suitable for arid and sandy zones.",
        "growing_season": "July - October (Kharif)",
        "ideal_conditions": "Low rainfall (30-60mm), High temp (25-32°C), Tolerates sandy soil",
        "economic_value": "Used in traditional savory snacks (bhujia) and as nutritious forage."
    },
    "mungbean": {
        "title": "Mung Bean / Green Gram (Vigna radiata)",
        "icon": "🫛",
        "category": "Short-duration Legume",
        "description": "Fast-maturing 60-day crop excellent for crop rotation and soil enrichment.",
        "growing_season": "Spring / Kharif / Summer",
        "ideal_conditions": "Warm temp (25-30°C), Moderate humidity, Low water requirement",
        "economic_value": "Quick cash crop between major cereal seasons."
    },
    "blackgram": {
        "title": "Blackgram / Urad (Vigna mungo)",
        "icon": "🌰",
        "category": "High-protein Pulse",
        "description": "Prefers warm humid regions with loamy soil rich in phosphorus.",
        "growing_season": "June - September",
        "ideal_conditions": "Temp 25-35°C, Moderate rainfall (60-90mm), pH 6.0-7.5",
        "economic_value": "Essential ingredient for batter products (idli/dosa) with steady demand."
    },
    "lentil": {
        "title": "Lentil / Masoor (Lens culinaris)",
        "icon": "🥣",
        "category": "Rabi Pulse",
        "description": "Cold-tolerant winter legume suited to alluvial and clay-loam soils.",
        "growing_season": "November - March",
        "ideal_conditions": "Cool temp (15-25°C), Low rainfall (40-60mm), Moderate NPK",
        "economic_value": "Nutrient-dense pulse with export opportunities."
    },
    "pomegranate": {
        "title": "Pomegranate (Punica granatum)",
        "icon": "🍎",
        "category": "Horticultural Fruit Crop",
        "description": "High-value fruit tree thriving in semi-arid and subtropical regions.",
        "growing_season": "Perennial (Flowers 3 seasons: Ambe, Mrig, Hasta)",
        "ideal_conditions": "Warm dry summer, cool winter, well-drained light soil, pH 6.5-7.5",
        "economic_value": "Exceptionally high ROI per hectare, export potential to Europe and Gulf."
    }
}

FERT_METADATA = {
    "Urea": {
        "formula": "CO(NH2)2",
        "npk": "46 - 0 - 0",
        "primary_nutrient": "Nitrogen (46%)",
        "description": "Highest nitrogen concentration among solid nitrogenous fertilizers. Rapid vegetative booster.",
        "usage_advice": "Apply during early growth stages. Avoid surface broadcasting without immediate watering or incorporation to prevent volatilization loss."
    },
    "DAP": {
        "formula": "Diammonium Phosphate (NH4)2HPO4",
        "npk": "18 - 46 - 0",
        "primary_nutrient": "Phosphorus (46%) + Nitrogen (18%)",
        "description": "Excellent basal fertilizer providing readily available phosphate for robust root establishment.",
        "usage_advice": "Place near seed furrow at planting time. Essential when soil test indicates severe phosphorus deficiency."
    },
    "14-35-14": {
        "formula": "NPK Complex Grade",
        "npk": "14 - 35 - 14",
        "primary_nutrient": "High Phosphorus Complex",
        "description": "Balanced high-phosphate fertilizer ideal for pulses, oilseeds, and root development in young plants.",
        "usage_advice": "Recommended for crops demanding early phosphorus boost combined with starting potassium support."
    },
    "28-28": {
        "formula": "Nitro-Phosphate Complex",
        "npk": "28 - 28 - 0",
        "primary_nutrient": "Equal Nitrogen & Phosphorus",
        "description": "High-potency dual nutrient formulation designed for vegetative spurt and energetic root vigor.",
        "usage_advice": "Suitable for sugarcane, paddy, and cotton during early tillering and vegetative branching."
    },
    "17-17-17": {
        "formula": "Standard Balanced NPK",
        "npk": "17 - 17 - 17",
        "primary_nutrient": "Fully Balanced (1:1:1)",
        "description": "Equally balanced all-around fertilizer suitable for maintenance dressing and general soil enrichment.",
        "usage_advice": "Ideal when soil analysis demonstrates uniform depletion across nitrogen, phosphorus, and potassium."
    },
    "20-20": {
        "formula": "Ammonium Phosphate Sulphate",
        "npk": "20 - 20 - 0 (+13% Sulphur)",
        "primary_nutrient": "Nitrogen + Phosphorus + Sulphur",
        "description": "Highly effective for oilseeds and cruciferous vegetables requiring active sulfur alongside N and P.",
        "usage_advice": "Boosts oil percentage in seeds and chlorophyll synthesis in green leaf canopies."
    },
    "10-26-26": {
        "formula": "Potassic Rich Complex",
        "npk": "10 - 26 - 26",
        "primary_nutrient": "High Phosphorus & Potassium",
        "description": "Formulated for fruit enlargement, grain filling, disease resistance, and lodging prevention.",
        "usage_advice": "Apply during reproductive and grain formation stages in cereal and sugarcane crops."
    }
}

# ============================================================
# REQUEST / RESPONSE SCHEMAS
# ============================================================
class CropPredictRequest(BaseModel):
    N: float = Field(..., description="Nitrogen content (ppm or kg/ha)", ge=0, le=200)
    P: float = Field(..., description="Phosphorus content (ppm or kg/ha)", ge=0, le=200)
    K: float = Field(..., description="Potassium content (ppm or kg/ha)", ge=0, le=200)
    temperature: float = Field(..., description="Temperature in Celsius", ge=0, le=60)
    humidity: float = Field(..., description="Relative humidity in percentage", ge=0, le=100)
    ph: float = Field(..., description="Soil pH value", ge=0, le=14)
    rainfall: float = Field(..., description="Rainfall in mm", ge=0, le=400)
    model_name: Optional[str] = "Random Forest"

class FertPredictRequest(BaseModel):
    Temperature: float = Field(..., description="Temperature in Celsius", ge=0, le=60)
    Humidity: float = Field(..., description="Relative humidity in percentage", ge=0, le=100)
    Moisture: float = Field(..., description="Soil moisture in percentage", ge=0, le=100)
    Soil_Type: str = Field(..., description="Soil type name")
    Crop_Type: str = Field(..., description="Crop type name")
    Nitrogen: float = Field(..., description="Nitrogen level in soil", ge=0, le=200)
    Phosphorous: float = Field(..., description="Phosphorus level in soil", ge=0, le=200)
    Potassium: float = Field(..., description="Potassium level in soil", ge=0, le=200)
    model_name: Optional[str] = "Random Forest"

# ============================================================
# API ROUTES
# ============================================================

@app.get("/api/status")
def get_status():
    return {
        "status": "online",
        "version": "2.0.0",
        "platform": "Crop & Fertilizer ML",
        "crop_models": list(crop_store["models"].keys()),
        "fertilizer_models": list(fert_store["models"].keys()),
        "crop_classes": crop_store["classes"],
        "fertilizer_classes": fert_store["classes"],
        "soil_types": fert_store["soil_types"],
        "crop_types": fert_store["crop_types"],
        "metrics": {
            "crop": crop_store["metrics"],
            "fertilizer": fert_store["metrics"]
        }
    }

@app.post("/api/predict/crop")
def predict_crop(req: CropPredictRequest):
    features = [req.N, req.P, req.K, req.temperature, req.humidity, req.ph, req.rainfall]
    X_input = np.array([features])
    X_scaled = crop_store["scaler"].transform(X_input)
    
    selected_model = req.model_name if req.model_name in crop_store["models"] else "Random Forest"
    model = crop_store["models"][selected_model]
    
    pred_class = model.predict(X_scaled)[0]
    
    # Probabilities
    probs = {}
    if hasattr(model, "predict_proba"):
        all_probs = model.predict_proba(X_scaled)[0]
        classes = model.classes_
        top_indices = np.argsort(all_probs)[::-1]
        for idx in top_indices:
            probs[classes[idx]] = round(float(all_probs[idx]) * 100, 2)
        confidence = probs.get(pred_class, 95.0)
    else:
        confidence = 90.0
        probs[pred_class] = confidence
        
    # Multi-model comparison
    comparison = {}
    for name, m in crop_store["models"].items():
        comp_pred = m.predict(X_scaled)[0]
        comp_conf = None
        if hasattr(m, "predict_proba"):
            c_probs = m.predict_proba(X_scaled)[0]
            c_idx = list(m.classes_).index(comp_pred)
            comp_conf = round(float(c_probs[c_idx]) * 100, 1)
        comparison[name] = {
            "predicted_crop": comp_pred,
            "confidence": comp_conf,
            "overall_accuracy": crop_store["metrics"][name]["accuracy"]
        }
        
    metadata = CROP_METADATA.get(pred_class.lower(), {
        "title": pred_class.capitalize(),
        "icon": "🌱",
        "category": "Agricultural Crop",
        "description": f"Recommended crop based on optimal environmental and soil nutrients matching {pred_class}.",
        "growing_season": "Standard agronomic cycle",
        "ideal_conditions": f"N={req.N}, P={req.P}, K={req.K}, Rainfall={req.rainfall}mm",
        "economic_value": "Commercial and subsistence agricultural product."
    })
    
    # Agronomic explanation
    reasons = []
    if req.rainfall > 150:
        reasons.append(f"High precipitation ({req.rainfall:.1f} mm) strongly favors water-intensive crops like {pred_class}.")
    elif req.rainfall < 70:
        reasons.append(f"Low rainfall ({req.rainfall:.1f} mm) is well-tolerated by drought-resilient crops like {pred_class}.")
        
    if req.N > 70:
        reasons.append(f"Abundant soil nitrogen ({req.N:.0f} ppm) supports the vigorous vegetative demands of {pred_class}.")
    elif req.N < 30:
        reasons.append(f"Low nitrogen requirement matches {pred_class}'s nitrogen-fixing or low-demand profile.")
        
    if req.ph < 6.0:
        reasons.append(f"Slightly acidic soil pH ({req.ph:.1f}) provides the optimal nutrient uptake window.")
    elif req.ph > 7.5:
        reasons.append(f"Alkaline tolerance matches {pred_class}'s root physiology.")
        
    if not reasons:
        reasons.append(f"All environmental parameters (N, P, K, pH, climate) align within the optimal standard deviation envelope for {pred_class}.")

    return {
        "success": True,
        "crop": pred_class,
        "confidence": confidence,
        "model_used": selected_model,
        "probabilities": probs,
        "multi_model_comparison": comparison,
        "metadata": metadata,
        "scientific_rationale": reasons
    }

@app.post("/api/predict/fertilizer")
def predict_fertilizer(req: FertPredictRequest):
    # Encode categoricals
    le_soil = fert_store["le_soil"]
    le_crop = fert_store["le_crop"]
    
    if req.Soil_Type not in le_soil.classes_:
        raise HTTPException(status_code=400, detail=f"Invalid Soil Type: {req.Soil_Type}. Valid: {list(le_soil.classes_)}")
    if req.Crop_Type not in le_crop.classes_:
        raise HTTPException(status_code=400, detail=f"Invalid Crop Type: {req.Crop_Type}. Valid: {list(le_crop.classes_)}")
        
    soil_enc = int(le_soil.transform([req.Soil_Type])[0])
    crop_enc = int(le_crop.transform([req.Crop_Type])[0])
    
    features = [
        req.Temperature, req.Humidity, req.Moisture,
        soil_enc, crop_enc,
        req.Nitrogen, req.Phosphorous, req.Potassium
    ]
    
    X_input = np.array([features])
    X_scaled = fert_store["scaler"].transform(X_input)
    
    selected_model = req.model_name if req.model_name in fert_store["models"] else "Random Forest"
    model = fert_store["models"][selected_model]
    
    pred_class = model.predict(X_scaled)[0]
    
    probs = {}
    if hasattr(model, "predict_proba"):
        all_probs = model.predict_proba(X_scaled)[0]
        classes = model.classes_
        top_indices = np.argsort(all_probs)[::-1]
        for idx in top_indices:
            probs[classes[idx]] = round(float(all_probs[idx]) * 100, 2)
        confidence = probs.get(pred_class, 95.0)
    else:
        confidence = 90.0
        probs[pred_class] = confidence
        
    comparison = {}
    for name, m in fert_store["models"].items():
        comp_pred = m.predict(X_scaled)[0]
        comp_conf = None
        if hasattr(m, "predict_proba"):
            c_probs = m.predict_proba(X_scaled)[0]
            c_idx = list(m.classes_).index(comp_pred)
            comp_conf = round(float(c_probs[c_idx]) * 100, 1)
        comparison[name] = {
            "predicted_fertilizer": comp_pred,
            "confidence": comp_conf,
            "overall_accuracy": fert_store["metrics"][name]["accuracy"]
        }
        
    metadata = FERT_METADATA.get(pred_class, {
        "formula": "Standard Formulation",
        "npk": "Commercial Compound",
        "primary_nutrient": "Balanced macro-nutrients",
        "description": f"Targeted chemical or organic fertilizer recommended to correct soil nutrient deficit for {req.Crop_Type}.",
        "usage_advice": "Incorporate evenly into topsoil and water thoroughly."
    })
    
    # Soil chemical diagnostics
    diagnostics = []
    if req.Nitrogen < 15:
        diagnostics.append(f"Critically low Nitrogen ({req.Nitrogen:.0f} ppm): Requires high-N corrective application.")
    if req.Phosphorous < 15:
        diagnostics.append(f"Phosphorus deficit ({req.Phosphorous:.0f} ppm): Inhibits seedling root establishment.")
    if req.Potassium < 15:
        diagnostics.append(f"Potassium deficit ({req.Potassium:.0f} ppm): Reduces drought resistance and crop vigor.")
    if req.Moisture < 30:
        diagnostics.append(f"Low moisture ({req.Moisture:.0f}%): Delay high-salt fertilizer application until soil is irrigated.")
        
    if not diagnostics:
        diagnostics.append(f"Soil nutrient profile is adequately buffered; {pred_class} recommended for seasonal crop uptake.")

    return {
        "success": True,
        "fertilizer": pred_class,
        "confidence": confidence,
        "model_used": selected_model,
        "probabilities": probs,
        "multi_model_comparison": comparison,
        "metadata": metadata,
        "diagnostics": diagnostics
    }

@app.get("/api/data/crop/sample")
def get_crop_sample(limit: int = 50):
    df = crop_store["df"]
    sample_df = df.sample(min(limit, len(df)), random_state=42)
    numeric_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    summary = {
        col: {
            "mean": round(float(df[col].mean()), 1),
            "min": round(float(df[col].min()), 1),
            "max": round(float(df[col].max()), 1)
        }
        for col in numeric_cols
    }
    return {
        "columns": list(df.columns),
        "data": sample_df.to_dict(orient="records"),
        "total_rows": len(df),
        "summary": summary
    }

@app.get("/api/data/fertilizer/sample")
def get_fert_sample(limit: int = 50):
    raw_cols = ["Temperature", "Humidity", "Moisture", "Soil Type", "Crop Type", "Nitrogen", "Phosphorous", "Potassium", "Fertilizer Name"]
    df = fert_store["df"][raw_cols]
    sample_df = df.sample(min(limit, len(df)), random_state=42)
    numeric_cols = ["Temperature", "Humidity", "Moisture", "Nitrogen", "Phosphorous", "Potassium"]
    summary = {
        col: {
            "mean": round(float(df[col].mean()), 1),
            "min": round(float(df[col].min()), 1),
            "max": round(float(df[col].max()), 1)
        }
        for col in numeric_cols
    }
    return {
        "columns": raw_cols,
        "data": sample_df.to_dict(orient="records"),
        "total_rows": len(df),
        "summary": summary
    }

@app.get("/api/metrics")
def get_metrics():
    return {
        "crop": crop_store["metrics"],
        "fertilizer": fert_store["metrics"]
    }

# ============================================================
# FARMER DECISION SUPPORT & GEO-INTELLIGENCE DATASETS
# ============================================================

LOCATION_PROFILES = {
    "chennai": {
        "name": "Chennai & Coastal Tamil Nadu",
        "state": "Tamil Nadu",
        "lat": 13.0827,
        "lng": 80.2707,
        "agro_zone": "East Coast Plains & Hills (ICAR Zone XI)",
        "soil_type": "Clayey Alluvial Loam & Coastal Sand",
        "avg_annual_rainfall_mm": 1200,
        "monsoon_profile": "North-East (Retreating) Monsoon peak (Oct-Dec ~65%), SW Monsoon (Jul-Sep ~30%)",
        "climate_classification": "Tropical Wet and Dry (Aw)",
        "current_weather": {
            "temperature": 29.5,
            "humidity": 78,
            "ph": 6.8,
            "rainfall": 240,
            "N": 85,
            "P": 42,
            "K": 48
        },
        "ndvi_vegetation_index": 0.68,
        "vegetation_status": "Healthy Dense Cropland Canopy",
        "historical_climate_summary": "10-year meteorological telemetry confirms high thermal stability (24-34°C) with significant NE monsoon rainfall. Coastal aquifer recharge creates favorable conditions for wet paddy, pulses, and sugarcane.",
        "top_historical_crops": ["Rice / Paddy", "Blackgram", "Groundnut", "Sugarcane"],
        "drought_risk": "Low to Moderate",
        "flood_risk": "Moderate during cyclonic depressions",
        "spectral_indices": {
            "ndvi": 0.68,
            "ndvi_status": "High Density Foliage",
            "ndwi": 0.42,
            "ndwi_status": "Optimal Hydration (No Canopy Water Stress)",
            "evi": 0.55,
            "evi_status": "High Vegetative Biomass Index",
            "soil_moisture_pct": 28.5,
            "soil_moisture_status": "28.5% Volumetric Topsoil Moisture",
            "canopy_temp_c": 27.2
        },
        "sowing_calendar": {
            "stage": "Samba Nursery Preparation & Direct Seeding",
            "optimal_window": "Oct 10 – Nov 15",
            "days_to_monsoon": 21,
            "monsoon_name": "North-East Monsoon Onset",
            "soil_workability": "Optimal for wet puddling & laser leveling"
        },
        "mandi_prices": [
            { "crop": "Paddy (Ponni Raw)", "mandi": "Koyambedu APMC", "price": 2480, "msp": 2300, "change": "+2.8%", "trend": "Bullish" },
            { "crop": "Blackgram (Urad)", "mandi": "Thiruvallur", "price": 7850, "msp": 7400, "change": "+1.5%", "trend": "Active" },
            { "crop": "Groundnut (Pods)", "mandi": "Kanchipuram", "price": 6920, "msp": 6783, "change": "+3.1%", "trend": "High Demand" },
            { "crop": "Sugarcane (Mill Gate)", "mandi": "Chengalpattu", "price": 3150, "msp": 3150, "change": "0.0%", "trend": "Stable FRP" }
        ],
        "social_web_feed": [
            {
                "platform": "X (Twitter)",
                "handle": "@TNAU_AgriExpert",
                "tag": "🚨 Pest Alert",
                "badge_class": "bg-rose-500/20 text-rose-300 border-rose-500/30",
                "title": "Stem Borer & Leaf Folder Early Monitoring Alert",
                "content": "Lowland coastal paddy in Thiruvallur & Kanchipuram: humid weather favored early leaf folder activity. Install 5 pheromone traps/acre. Refrain from excess urea top-dressing.",
                "timestamp": "2h ago",
                "meta": "184 Reposts • Verified Agronomist"
            },
            {
                "platform": "Reddit",
                "handle": "r/IndianAgriculture • u/tamil_delta_tech",
                "tag": "🌱 Verified Field Test",
                "badge_class": "bg-almond/20 text-almond border-almond/30",
                "title": "SRI Paddy Trial with Azospirillum Coating",
                "content": "Tested Co-51 seed treatment with liquid bio-fertilizer Azospirillum + Phosphobacteria. Tiller count increased by 30% with 25 kg/acre reduction in synthetic Urea.",
                "timestamp": "5h ago",
                "meta": "312 Upvotes • 48 Comments"
            },
            {
                "platform": "e-NAM Web",
                "handle": "Tamil Nadu Regulated Markets",
                "tag": "📈 Mandi Price Radar",
                "badge_class": "bg-matcha/20 text-matcha border-matcha/30",
                "title": "Blackgram Procurement Crossing 1,800 Q Daily",
                "content": "Moisture threshold strictly pegged at 12%. High miller buying interest for export-grade whole urad. Farmers advised to dry harvest under shaded tarpaulins.",
                "timestamp": "7h ago",
                "meta": "Official APMC Bulletin"
            }
        ]
    },
    "thanjavur": {
        "name": "Thanjavur (Cauvery Delta Rice Bowl)",
        "state": "Tamil Nadu",
        "lat": 10.7870,
        "lng": 79.1378,
        "agro_zone": "Cauvery Deltaic Zone",
        "soil_type": "Deep Heavy Clay Alluvium (Regur/Clayey)",
        "avg_annual_rainfall_mm": 1050,
        "monsoon_profile": "NE Monsoon peak (Oct-Dec), Canal irrigation fed by Cauvery Mettur dam",
        "climate_classification": "Tropical Semi-Arid to Sub-Humid",
        "current_weather": {
            "temperature": 28.0,
            "humidity": 80,
            "ph": 6.7,
            "rainfall": 210,
            "N": 92,
            "P": 45,
            "K": 40
        },
        "ndvi_vegetation_index": 0.74,
        "vegetation_status": "Intense Paddy Field Canopy",
        "historical_climate_summary": "Century-long multi-cropping history with Kuruvai, Samba, and Thaladi rice seasons followed by blackgram pulse fallow.",
        "top_historical_crops": ["Rice", "Blackgram", "Banana", "Sugarcane"],
        "drought_risk": "Moderate (Dependent on river inflows)",
        "flood_risk": "Moderate in low-lying delta canals",
        "spectral_indices": {
            "ndvi": 0.74,
            "ndvi_status": "Peak Vegetative Canopy",
            "ndwi": 0.52,
            "ndwi_status": "High Surface Water Content (Puddled Soil)",
            "evi": 0.62,
            "evi_status": "Very High Biomass Index",
            "soil_moisture_pct": 34.0,
            "soil_moisture_status": "34.0% Saturated Clay Moisture",
            "canopy_temp_c": 26.5
        },
        "sowing_calendar": {
            "stage": "Samba Paddy Main Field Transplanting",
            "optimal_window": "Sep 25 – Oct 30",
            "days_to_monsoon": 18,
            "monsoon_name": "Cauvery Peak Discharge Window",
            "soil_workability": "Ideal for mechanical rice transplanter"
        },
        "mandi_prices": [
            { "crop": "Paddy (CR-1009 / ADT-45)", "mandi": "Thanjavur Regulated", "price": 2420, "msp": 2300, "change": "+2.1%", "trend": "Bullish" },
            { "crop": "Blackgram (Vamban-8)", "mandi": "Kumbakonam", "price": 8100, "msp": 7400, "change": "+4.2%", "trend": "High Demand" },
            { "crop": "Banana (Robusta)", "mandi": "Papanasam", "price": 1850, "msp": 1700, "change": "+1.2%", "trend": "Stable" },
            { "crop": "Sesame (Til)", "mandi": "Orathanadu", "price": 13400, "msp": 9267, "change": "+3.5%", "trend": "Strong Gain" }
        ],
        "social_web_feed": [
            {
                "platform": "X (Twitter)",
                "handle": "@CauveryKisanCell",
                "tag": "💧 Canal Water Release",
                "badge_class": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
                "title": "Mettur Dam Discharge Maintained at 18,500 Cusecs",
                "content": "Grand Anicut water levels adequate for tail-end branches in Tiruvarur & Nagapattinam. Farmers advised to complete basal NPK application within next 5 days.",
                "timestamp": "1h ago",
                "meta": "240 Reposts • Water Resources Dept"
            },
            {
                "platform": "Reddit",
                "handle": "r/farming • u/delta_grain_master",
                "tag": "🚨 Pest & Fungal Alert",
                "badge_class": "bg-rose-500/20 text-rose-300 border-rose-500/30",
                "title": "Sheath Blight & Bacterial Leaf Streak Watch",
                "content": "Cloudy overcast mornings in Needamangalam triggered sheath blight patches. Keep bunds weed-free and spray Pseudomonas fluorescens 10g/L early morning.",
                "timestamp": "4h ago",
                "meta": "195 Upvotes • 32 Comments"
            },
            {
                "platform": "KVK Bulletin",
                "handle": "ICAR-KVK Needamangalam",
                "tag": "🌱 Micro-Nutrient Advisory",
                "badge_class": "bg-almond/20 text-almond border-almond/30",
                "title": "Zinc Sulphate Basal Application Mandatory for Clay",
                "content": "Deltaic clay soils show acute zinc immobilization under flooded conditions. Broadcast 25 kg Zinc Sulphate mixed with sand; do not mix directly with DAP.",
                "timestamp": "6h ago",
                "meta": "Certified Extension Guide"
            }
        ]
    },
    "coimbatore": {
        "name": "Coimbatore & Western Tamil Nadu",
        "state": "Tamil Nadu",
        "lat": 11.0168,
        "lng": 76.9558,
        "agro_zone": "Western Agro-Climatic Zone",
        "soil_type": "Red Gravelly / Black Calcareous Soil",
        "avg_annual_rainfall_mm": 680,
        "monsoon_profile": "Rain-shadow plateau, moderate SW and NE monsoon",
        "climate_classification": "Semi-Arid Tropical",
        "current_weather": {
            "temperature": 26.5,
            "humidity": 65,
            "ph": 7.2,
            "rainfall": 95,
            "N": 65,
            "P": 38,
            "K": 55
        },
        "ndvi_vegetation_index": 0.62,
        "vegetation_status": "Moderate Semi-Arid Foliage",
        "historical_climate_summary": "High suitability for drought-hardy pulses, cotton, maize, and millets with drip irrigation support.",
        "top_historical_crops": ["Maize", "Cotton", "Sorghum", "Groundnut"],
        "drought_risk": "High in dry summer months",
        "flood_risk": "Very Low",
        "spectral_indices": {
            "ndvi": 0.62,
            "ndvi_status": "Moderate Foliage Density",
            "ndwi": 0.28,
            "ndwi_status": "Mild Moisture Deficit (Drip Support Required)",
            "evi": 0.44,
            "evi_status": "Spaced Canopy Row-Crop Signature",
            "soil_moisture_pct": 16.8,
            "soil_moisture_status": "16.8% Volumetric Moisture",
            "canopy_temp_c": 29.8
        },
        "sowing_calendar": {
            "stage": "Maize Whorl Formation & Cotton Flowering",
            "optimal_window": "Jul 15 – Aug 25",
            "days_to_monsoon": 40,
            "monsoon_name": "Rain-Shadow Light Showers",
            "soil_workability": "Friable dry loam, excellent for micro-fertigation"
        },
        "mandi_prices": [
            { "crop": "Maize (Yellow Hybrid)", "mandi": "Coimbatore APMC", "price": 2320, "msp": 2225, "change": "+3.8%", "trend": "Bullish" },
            { "crop": "Cotton (Medium Staple)", "mandi": "Tirupur Regulated", "price": 7450, "msp": 7121, "change": "+1.9%", "trend": "Active" },
            { "crop": "Turmeric (Finger Erode)", "mandi": "Pollachi", "price": 14200, "msp": 9000, "change": "+6.4%", "trend": "Strong Rally" },
            { "crop": "Sorghum (Jowar)", "mandi": "Udumalpet", "price": 3350, "msp": 3180, "change": "+1.1%", "trend": "Stable" }
        ],
        "social_web_feed": [
            {
                "platform": "X (Twitter)",
                "handle": "@TNAU_CropSurveillance",
                "tag": "🚨 Fall Armyworm Alert",
                "badge_class": "bg-rose-500/20 text-rose-300 border-rose-500/30",
                "title": "Spodoptera frugiperda Detection in Hybrid Maize",
                "content": "Larval feeding noticed in maize whorls in Pollachi & Sulur. Spray Emamectin Benzoate 5% SG @ 0.4g/L or Chlorantraniliprole 18.5% SC @ 0.3ml/L directed into central whorls.",
                "timestamp": "2h ago",
                "meta": "215 Reposts • Entomologist Advisory"
            },
            {
                "platform": "Reddit",
                "handle": "r/IndianAgriculture • u/kongu_drip_pioneer",
                "tag": "💡 Drip Fertigation Efficiency",
                "badge_class": "bg-almond/20 text-almond border-almond/30",
                "title": "Subsurface Drip Irrigation on Red Soils",
                "content": "Transitioned to venturi fertigation with 19:19:19 water-soluble grade on 4 acres cotton. Water consumption cut by 45%, electrical pumping hours reduced to 2.5 hrs/day.",
                "timestamp": "5h ago",
                "meta": "420 Upvotes • 56 Comments"
            },
            {
                "platform": "Agri-Industry Web",
                "handle": "Poultry Feed Association FeedWatch",
                "tag": "📈 Feed Procurement Demand",
                "badge_class": "bg-matcha/20 text-matcha border-matcha/30",
                "title": "Feed Millers Actively Buying Maize with <14% Moisture",
                "content": "Poultry hubs in Palladam & Namakkal offering ₹60/Q premium over spot prices for test weight >720g/L and zero aflatoxin contamination.",
                "timestamp": "8h ago",
                "meta": "Verified Buyer Feed"
            }
        ]
    },
    "ludhiana": {
        "name": "Ludhiana (Central Plain Punjab)",
        "state": "Punjab",
        "lat": 30.9010,
        "lng": 75.8573,
        "agro_zone": "Trans-Gangetic Plains (Zone VI)",
        "soil_type": "Deep Loamy Alluvium (Indo-Gangetic)",
        "avg_annual_rainfall_mm": 700,
        "monsoon_profile": "SW Monsoon (Jul-Aug) + Western Disturbances (Winter rains)",
        "climate_classification": "Subtropical Semi-Arid",
        "current_weather": {
            "temperature": 22.0,
            "humidity": 60,
            "ph": 7.4,
            "rainfall": 110,
            "N": 105,
            "P": 48,
            "K": 35
        },
        "ndvi_vegetation_index": 0.78,
        "vegetation_status": "High Agricultural Vigor",
        "historical_climate_summary": "Wheat-Paddy intensive cropping system with canal and deep tube-well infrastructure.",
        "top_historical_crops": ["Wheat", "Rice", "Maize", "Mustard"],
        "drought_risk": "Low (High groundwater pumping dependency)",
        "flood_risk": "Low",
        "spectral_indices": {
            "ndvi": 0.78,
            "ndvi_status": "Very High Biomass Signature",
            "ndwi": 0.48,
            "ndwi_status": "Adequate Subsurface Hydration",
            "evi": 0.68,
            "evi_status": "Dense Multi-Canopy Profile",
            "soil_moisture_pct": 26.2,
            "soil_moisture_status": "26.2% Tube-well Maintained Alluvium",
            "canopy_temp_c": 24.1
        },
        "sowing_calendar": {
            "stage": "Paddy Combine Harvesting & Rabi Wheat Seeding",
            "optimal_window": "Oct 25 – Nov 20",
            "days_to_monsoon": 75,
            "monsoon_name": "Winter Western Disturbances Expected",
            "soil_workability": "Super Seeder direct drilling into standing stubble"
        },
        "mandi_prices": [
            { "crop": "Basmati 1121 Paddy", "mandi": "Khanna APMC", "price": 3950, "msp": 2300, "change": "+4.5%", "trend": "Bullish Export Demand" },
            { "crop": "Wheat (Sharbati / PBW)", "mandi": "Ludhiana Mandi", "price": 2425, "msp": 2275, "change": "+1.8%", "trend": "Stable" },
            { "crop": "Mustard (Sarson)", "mandi": "Jagraon", "price": 5850, "msp": 5650, "change": "+2.2%", "trend": "Active" },
            { "crop": "Maize (Kharif Grain)", "mandi": "Samrala", "price": 2180, "msp": 2225, "change": "-0.5%", "trend": "Moderate" }
        ],
        "social_web_feed": [
            {
                "platform": "X (Twitter)",
                "handle": "@PAU_Extension",
                "tag": "🌾 Wheat Seed Variety Advisory",
                "badge_class": "bg-almond/20 text-almond border-almond/30",
                "title": "PBW-826 & DBW-303 Heat-Tolerant Cultivars Recommended",
                "content": "PAU agronomists urge farmers to seed heat-resilient wheat strains to counter potential February terminal heat spikes. Treat seed with Trichoderma viride @ 4g/kg.",
                "timestamp": "1h ago",
                "meta": "530 Reposts • Punjab Agricultural University"
            },
            {
                "platform": "Reddit",
                "handle": "r/farming • u/punjab_seeder_mechanic",
                "tag": "🚜 In-Situ Straw Management",
                "badge_class": "bg-matcha/20 text-matcha border-matcha/30",
                "title": "Direct Seeding Wheat with Happy Seeder",
                "content": "Zero residue burning on our 20-acre block for 4 seasons straight. Retained paddy straw mulch saved 1 irrigation cycle and completely suppressed Phalaris minor weeds.",
                "timestamp": "3h ago",
                "meta": "640 Upvotes • 82 Comments"
            },
            {
                "platform": "X #PunjabKisan",
                "handle": "@KisanMandiReporter",
                "tag": "📈 Khanna Mandi Arrival Surge",
                "badge_class": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
                "title": "Record 45,000 Bags of Basmati Traded in Khanna",
                "content": "High quality export consignments securing ₹3,950/Q. Moisture testing strictly computerized with direct farmer bank payment within 24 hours.",
                "timestamp": "6h ago",
                "meta": "Official Mandi Board Report"
            }
        ]
    },
    "nashik": {
        "name": "Nashik & Western Maharashtra",
        "state": "Maharashtra",
        "lat": 19.9975,
        "lng": 73.7898,
        "agro_zone": "Western Plateau & Hills (Zone IX)",
        "soil_type": "Deep Black Basaltic Soil (Regur)",
        "avg_annual_rainfall_mm": 850,
        "monsoon_profile": "SW Monsoon heavy (Jun-Sep)",
        "climate_classification": "Tropical Wet-Dry",
        "current_weather": {
            "temperature": 24.5,
            "humidity": 70,
            "ph": 6.9,
            "rainfall": 140,
            "N": 70,
            "P": 44,
            "K": 60
        },
        "ndvi_vegetation_index": 0.69,
        "vegetation_status": "Active Horticultural & Field Crops",
        "historical_climate_summary": "Black moisture-retentive basaltic soils with high cation exchange capacity.",
        "top_historical_crops": ["Cotton", "Sugarcane", "Pigeonpeas", "Chickpea"],
        "drought_risk": "Moderate",
        "flood_risk": "Low",
        "spectral_indices": {
            "ndvi": 0.69,
            "ndvi_status": "Active Horticultural Canopy",
            "ndwi": 0.38,
            "ndwi_status": "Moderate Leaf Moisture Balance",
            "evi": 0.52,
            "evi_status": "Vigorous Vineyard / Onion Foliage",
            "soil_moisture_pct": 24.0,
            "soil_moisture_status": "24.0% Black Basaltic Moisture",
            "canopy_temp_c": 26.8
        },
        "sowing_calendar": {
            "stage": "Late Kharif Red Onion Transplanting & Grape Pruning",
            "optimal_window": "Oct 1 – Nov 15",
            "days_to_monsoon": 60,
            "monsoon_name": "Post-Monsoon Winter Dew Regime",
            "soil_workability": "Black vertisol rotary tilling for raised bed forming"
        },
        "mandi_prices": [
            { "crop": "Red Onion (Kharif Pola)", "mandi": "Lasalgaon APMC", "price": 2850, "msp": 1950, "change": "+5.8%", "trend": "Sharp Price Spike" },
            { "crop": "Table Grapes (Thompson)", "mandi": "Pimpalgaon", "price": 6500, "msp": 4500, "change": "+3.4%", "trend": "Early Premium" },
            { "crop": "Soyabean (Yellow)", "mandi": "Malegaon", "price": 4850, "msp": 4892, "change": "-0.8%", "trend": "High Arrival" },
            { "crop": "Chickpea (Chana Desi)", "mandi": "Yeola", "price": 6100, "msp": 5440, "change": "+3.2%", "trend": "Bullish" }
        ],
        "social_web_feed": [
            {
                "platform": "X (Twitter)",
                "handle": "@MahaGrapeWatch",
                "tag": "🚨 Downy Mildew Precaution",
                "badge_class": "bg-rose-500/20 text-rose-300 border-rose-500/30",
                "title": "Night Dew & Temperature Drop Threatening Vineyards",
                "content": "Night humidity >85% creating infection window for Plasmopara viticola. Spray Potassium Salt of Phosphonic Acid @ 3g/L or Bordeaux mixture 0.8% immediately after pruning.",
                "timestamp": "2h ago",
                "meta": "340 Reposts • Grape Growers Association"
            },
            {
                "platform": "Reddit",
                "handle": "r/IndianAgriculture • u/onion_valley_grower",
                "tag": "🧅 Kharif Onion Raised Bed Protocol",
                "badge_class": "bg-almond/20 text-almond border-almond/30",
                "title": "Collar Rot Prevention on Black Cotton Soil",
                "content": "Planting on 120cm broad beds with silver-black plastic mulch and drip lines. Zero water stagnation, bulb grading uniformity increased to 92% A-Grade.",
                "timestamp": "4h ago",
                "meta": "512 Upvotes • 71 Comments"
            },
            {
                "platform": "e-NAM / Lasalgaon APMC",
                "handle": "@LasalgaonMandiLive",
                "tag": "📈 Onion Auction Rates Top ₹2,850/Q",
                "badge_class": "bg-matcha/20 text-matcha border-matcha/30",
                "title": "Robust Out-of-State Purchasing from South India",
                "content": "Modal wholesale price reached ₹2,850/Q today across 18,000 quintal arrivals. Southern rail rakes actively loading at Niphad siding.",
                "timestamp": "7h ago",
                "meta": "Official APMC Market Feed"
            }
        ]
    }
}


CROP_ECONOMICS = {
    "rice": { "name": "Rice / Paddy", "avg_yield_q_per_acre": 22.0, "msp_per_q": 2300, "cost_per_acre": 24500, "market_demand": "Very High", "risk_level": "Low" },
    "maize": { "name": "Maize / Corn", "avg_yield_q_per_acre": 25.0, "msp_per_q": 2225, "cost_per_acre": 21000, "market_demand": "High", "risk_level": "Low" },
    "chickpea": { "name": "Chickpea / Bengal Gram", "avg_yield_q_per_acre": 8.5, "msp_per_q": 5440, "cost_per_acre": 17500, "market_demand": "High", "risk_level": "Low" },
    "kidneybeans": { "name": "Kidney Beans / Rajma", "avg_yield_q_per_acre": 7.0, "msp_per_q": 7200, "cost_per_acre": 19000, "market_demand": "High", "risk_level": "Medium" },
    "pigeonpeas": { "name": "Pigeonpeas / Tur Dal", "avg_yield_q_per_acre": 7.5, "msp_per_q": 7550, "cost_per_acre": 18500, "market_demand": "Very High", "risk_level": "Medium" },
    "mothbeans": { "name": "Moth Beans", "avg_yield_q_per_acre": 5.5, "msp_per_q": 6800, "cost_per_acre": 12000, "market_demand": "Moderate", "risk_level": "Low" },
    "mungbean": { "name": "Mung Bean / Green Gram", "avg_yield_q_per_acre": 6.0, "msp_per_q": 8558, "cost_per_acre": 16000, "market_demand": "High", "risk_level": "Low" },
    "blackgram": { "name": "Black Gram / Urad Dal", "avg_yield_q_per_acre": 6.5, "msp_per_q": 7400, "cost_per_acre": 15500, "market_demand": "Very High", "risk_level": "Low" },
    "lentil": { "name": "Lentil / Masoor", "avg_yield_q_per_acre": 6.8, "msp_per_q": 6425, "cost_per_acre": 15000, "market_demand": "High", "risk_level": "Low" },
    "pomegranate": { "name": "Pomegranate", "avg_yield_q_per_acre": 45.0, "msp_per_q": 5500, "cost_per_acre": 65000, "market_demand": "High", "risk_level": "Medium" },
    "banana": { "name": "Banana", "avg_yield_q_per_acre": 180.0, "msp_per_q": 1400, "cost_per_acre": 85000, "market_demand": "Very High", "risk_level": "Medium" },
    "mango": { "name": "Mango Orchard", "avg_yield_q_per_acre": 35.0, "msp_per_q": 4500, "cost_per_acre": 40000, "market_demand": "High", "risk_level": "Medium" },
    "grapes": { "name": "Grapes", "avg_yield_q_per_acre": 80.0, "msp_per_q": 3800, "cost_per_acre": 95000, "market_demand": "High", "risk_level": "High" },
    "watermelon": { "name": "Watermelon", "avg_yield_q_per_acre": 120.0, "msp_per_q": 900, "cost_per_acre": 35000, "market_demand": "Moderate", "risk_level": "Medium" },
    "muskmelon": { "name": "Muskmelon", "avg_yield_q_per_acre": 90.0, "msp_per_q": 1100, "cost_per_acre": 32000, "market_demand": "Moderate", "risk_level": "Medium" },
    "apple": { "name": "Apple", "avg_yield_q_per_acre": 50.0, "msp_per_q": 6000, "cost_per_acre": 80000, "market_demand": "High", "risk_level": "High" },
    "orange": { "name": "Orange / Citrus", "avg_yield_q_per_acre": 60.0, "msp_per_q": 3200, "cost_per_acre": 45000, "market_demand": "High", "risk_level": "Medium" },
    "papaya": { "name": "Papaya", "avg_yield_q_per_acre": 140.0, "msp_per_q": 1200, "cost_per_acre": 50000, "market_demand": "High", "risk_level": "Medium" },
    "coconut": { "name": "Coconut (Nuts/Acre)", "avg_yield_q_per_acre": 50.0, "msp_per_q": 3000, "cost_per_acre": 30000, "market_demand": "Very High", "risk_level": "Low" },
    "cotton": { "name": "Cotton", "avg_yield_q_per_acre": 9.5, "msp_per_q": 7121, "cost_per_acre": 28000, "market_demand": "High", "risk_level": "Medium" },
    "jute": { "name": "Jute", "avg_yield_q_per_acre": 14.0, "msp_per_q": 5050, "cost_per_acre": 22000, "market_demand": "Moderate", "risk_level": "Low" },
    "coffee": { "name": "Coffee Plantation", "avg_yield_q_per_acre": 8.0, "msp_per_q": 18000, "cost_per_acre": 55000, "market_demand": "High", "risk_level": "Medium" }
}

FERTILIZER_DOSAGE_GUIDELINES = {
    "Urea": { "bag_weight_kg": 50, "avg_bags_per_acre": 2.5, "cost_per_bag_inr": 268, "timing": "1 bag basal at sowing + 1.5 bags split in two top-dressings at 30 and 50 days.", "excess_risk": "Severe Soil Acidification & Nitrate Leaching. Excess creates soft lush foliage highly vulnerable to fungal blight." },
    "DAP": { "bag_weight_kg": 50, "avg_bags_per_acre": 1.5, "cost_per_bag_inr": 1350, "timing": "100% basal application placed in furrows 5 cm below seed depth.", "excess_risk": "Fixation of zinc and iron in alkaline soils; phosphate immobilization." },
    "14-35-14": { "bag_weight_kg": 50, "avg_bags_per_acre": 2.0, "cost_per_bag_inr": 1450, "timing": "Full basal dose during final land preparation before irrigation.", "excess_risk": "Over-fertilization raises electrical conductivity (salinity spike), retarding seedling emergence." },
    "28-28": { "bag_weight_kg": 50, "avg_bags_per_acre": 2.0, "cost_per_bag_inr": 1400, "timing": "50% basal at sowing + 50% top-dressing at tillering stage.", "excess_risk": "High vegetative surge; lodging risk in tall cereals." },
    "17-17-17": { "bag_weight_kg": 50, "avg_bags_per_acre": 2.5, "cost_per_bag_inr": 1380, "timing": "Balanced NPK: half at sowing, half at panicle initiation.", "excess_risk": "Moderate salinity risk under dry spell conditions." },
    "20-20": { "bag_weight_kg": 50, "avg_bags_per_acre": 2.0, "cost_per_bag_inr": 1250, "timing": "Basal application for oilseeds and legumes.", "excess_risk": "Sulfur imbalance if used without soil test." },
    "10-26-26": { "bag_weight_kg": 50, "avg_bags_per_acre": 2.0, "cost_per_bag_inr": 1470, "timing": "Excellent potassic booster for sugarcane and tuber crops.", "excess_risk": "Magnesium deficiency through competitive potassium antagonism." }
}

# Request Schemas
class FarmerProfitRequest(BaseModel):
    crop_name: str
    land_area_acres: float = Field(2.5, ge=0.1, le=1000.0)

class FarmerDosageRequest(BaseModel):
    fertilizer_name: str
    crop_name: Optional[str] = "Rice"
    soil_type: Optional[str] = "Loamy"
    land_area_acres: float = Field(2.5, ge=0.1, le=1000.0)

# ============================================================
# NEW API ENDPOINTS: GEO-LOCATION & FARMER DECISION TOOLS
# ============================================================

@app.get("/api/geo/analyze")
def analyze_geo_location(location: str = "chennai"):
    loc_key = location.lower().strip()
    profile = LOCATION_PROFILES.get(loc_key)
    if not profile:
        for k, v in LOCATION_PROFILES.items():
            if k in loc_key or loc_key in k:
                profile = v
                break
    if not profile:
        profile = LOCATION_PROFILES["chennai"]
    
    return {
        "success": True,
        "name": profile["name"],
        "state": profile["state"],
        "lat": profile["lat"],
        "lng": profile["lng"],
        "ndvi_score": profile["ndvi_vegetation_index"],
        "vegetation_status": profile["vegetation_status"],
        "telemetry": profile["current_weather"],
        "historical_telemetry": {
            "annual_rainfall_mm": profile["avg_annual_rainfall_mm"],
            "mean_temperature_c": profile["current_weather"]["temperature"],
            "climate_hazard_risk": profile.get("flood_risk", "Moderate")
        },
        "spectral_indices": profile.get("spectral_indices", {}),
        "mandi_prices": profile.get("mandi_prices", []),
        "social_web_feed": profile.get("social_web_feed", []),
        "sowing_calendar": profile.get("sowing_calendar", {}),
        "location_profile": profile
    }

@app.post("/api/farmer/profitability")
def calculate_profitability(req: FarmerProfitRequest):
    crop_key = req.crop_name.lower().strip()
    econ = CROP_ECONOMICS.get(crop_key, {
        "name": req.crop_name.capitalize(),
        "avg_yield_q_per_acre": 15.0,
        "msp_per_q": 3500,
        "cost_per_acre": 22000,
        "market_demand": "High",
        "risk_level": "Low"
    })
    
    acres = req.land_area_acres
    total_yield = round(econ["avg_yield_q_per_acre"] * acres, 1)
    gross_revenue = round(total_yield * econ["msp_per_q"], 0)
    total_cost = round(econ["cost_per_acre"] * acres, 0)
    net_profit = round(gross_revenue - total_cost, 0)
    roi = round((net_profit / total_cost) * 100, 1) if total_cost > 0 else 0
    
    return {
        "success": True,
        "crop": req.crop_name,
        "crop_display": econ["name"],
        "land_area_acres": acres,
        "expected_yield_quintals": total_yield,
        "yield_per_acre": econ["avg_yield_q_per_acre"],
        "msp_per_quintal": econ["msp_per_q"],
        "gross_revenue_inr": gross_revenue,
        "production_cost_inr": total_cost,
        "net_profit_inr": net_profit,
        "roi_percentage": roi,
        "market_demand": econ["market_demand"],
        "risk_level": econ["risk_level"]
    }

@app.post("/api/farmer/fertilizer-dosage")
def calculate_fertilizer_dosage(req: FarmerDosageRequest):
    fert_key = req.fertilizer_name.strip()
    guide = FERTILIZER_DOSAGE_GUIDELINES.get(fert_key, {
        "bag_weight_kg": 50,
        "avg_bags_per_acre": 2.0,
        "cost_per_bag_inr": 1200,
        "timing": "Apply evenly in split doses: half at sowing and half at vegetative growth.",
        "excess_risk": "Moderate salinity risk if applied in drought conditions."
    })
    
    acres = req.land_area_acres
    total_bags = round(guide["avg_bags_per_acre"] * acres, 1)
    total_weight_kg = round(total_bags * guide["bag_weight_kg"], 1)
    total_cost_inr = round(total_bags * guide["cost_per_bag_inr"], 0)
    
    conventional_bags = round(total_bags * 1.8, 1)
    conventional_cost = round(conventional_bags * guide["cost_per_bag_inr"], 0)
    savings_inr = round(conventional_cost - total_cost_inr, 0)
    
    return {
        "success": True,
        "fertilizer": req.fertilizer_name,
        "land_area_acres": acres,
        "recommended_bags_50kg": total_bags,
        "total_weight_kg": total_weight_kg,
        "estimated_cost_inr": total_cost_inr,
        "conventional_overuse_bags": conventional_bags,
        "estimated_savings_inr": savings_inr,
        "application_schedule": guide["timing"],
        "excess_toxicity_risk": guide["excess_risk"],
        "eco_rating": "Optimized Chemical Efficiency"
    }

@app.post("/api/farmer/climate-stress")
def simulate_climate_stress(req: CropPredictRequest):
    rf_model = crop_store["models"]["Random Forest"]
    scaler = crop_store["scaler"]
    
    scenarios = [
        {
            "id": "drought",
            "name": "Severe 30% Drought Shock",
            "icon": "☀️",
            "description": "Simulates failure of monsoon rains (-30% precipitation) combined with +1.5°C temperature rise.",
            "N": req.N, "P": req.P, "K": req.K,
            "temperature": min(req.temperature + 1.5, 45.0),
            "humidity": max(req.humidity * 0.75, 20.0),
            "ph": req.ph,
            "rainfall": max(req.rainfall * 0.70, 15.0)
        },
        {
            "id": "heatwave",
            "name": "+3.5°C Extreme Heatwave Shock",
            "icon": "🔥",
            "description": "Simulates unseasonal spring heat spikes during flowering/grain filling stage.",
            "N": req.N, "P": req.P, "K": req.K,
            "temperature": min(req.temperature + 3.5, 48.0),
            "humidity": max(req.humidity * 0.85, 20.0),
            "ph": req.ph,
            "rainfall": req.rainfall
        },
        {
            "id": "excess_rain",
            "name": "+50% Cyclonic Cloudburst",
            "icon": "🌧️",
            "description": "Simulates extreme rainfall anomalies leading to water-logging and soil saturation.",
            "N": req.N, "P": req.P, "K": req.K,
            "temperature": max(req.temperature - 1.5, 15.0),
            "humidity": min(req.humidity * 1.15, 98.0),
            "ph": req.ph,
            "rainfall": min(req.rainfall * 1.50, 350.0)
        }
    ]
    
    results = []
    for sc in scenarios:
        feat = [sc["N"], sc["P"], sc["K"], sc["temperature"], sc["humidity"], sc["ph"], sc["rainfall"]]
        x_scaled = scaler.transform([feat])
        pred = rf_model.predict(x_scaled)[0]
        probs = rf_model.predict_proba(x_scaled)[0]
        c_idx = list(rf_model.classes_).index(pred)
        conf = round(float(probs[c_idx]) * 100, 1)
        
        results.append({
            "scenario_id": sc["id"],
            "scenario_name": sc["name"],
            "icon": sc["icon"],
            "description": sc["description"],
            "simulated_params": {
                "temperature": round(sc["temperature"], 1),
                "humidity": round(sc["humidity"], 1),
                "rainfall": round(sc["rainfall"], 1)
            },
            "predicted_resilient_crop": pred,
            "confidence": conf,
            "crop_meta": CROP_METADATA.get(pred.lower(), {})
        })
        
    return {
        "success": True,
        "scenarios": results
    }

@app.get("/api/farmer/crop-rotation")
def get_crop_rotation(crop_name: str = "rice"):
    crop_lower = crop_name.lower().strip()
    
    if crop_lower in ["rice", "paddy"]:
        cycle = {
            "primary_crop": "Rice / Paddy (Kharif Monsoon)",
            "season_1": { "name": "Rice / Paddy", "season": "Kharif (June - Oct)", "role": "Heavy nutrient feeder; requires puddle clayey soil." },
            "season_2": { "name": "Blackgram / Chickpea", "season": "Rabi (Nov - Feb)", "role": "Rhizobial Nitrogen Fixation (+40 kg N/ha restored naturally; breaks soil compaction)." },
            "season_3": { "name": "Sesbania (Dhaincha) / Green Manure", "season": "Summer (Mar - May)", "role": "Incorporate green biomass into soil; boosts organic carbon by 0.3%." },
            "benefits": ["Naturally regenerates 40 kg Nitrogen per hectare", "Breaks stem-borer and gall midge pest cycles", "Improves water infiltration for next monsoon"]
        }
    elif crop_lower in ["chickpea", "mungbean", "blackgram", "pigeonpeas", "kidneybeans", "lentil", "mothbeans"]:
        cycle = {
            "primary_crop": f"{crop_name.capitalize()} (Legume Nitrogen Booster)",
            "season_1": { "name": f"{crop_name.capitalize()}", "season": "Current Season", "role": "Biological nitrogen fixation via root nodules." },
            "season_2": { "name": "Maize / Wheat", "season": "Next Season", "role": "Capitalizes on residual nitrogen reserves in topsoil." },
            "season_3": { "name": "Mustard / Fodder Sorghum", "season": "Third Season", "role": "Deep-root pest sanitization and bio-fumigation." },
            "benefits": ["Maximizes residual nitrogen uptake", "Reduces synthetic Urea requirement by 35%", "Maintains balanced soil macro-biology"]
        }
    elif crop_lower in ["cotton", "jute"]:
        cycle = {
            "primary_crop": "Cotton / Fiber Crop",
            "season_1": { "name": "Cotton", "season": "Kharif to Winter (Long Duration)", "role": "High potassium and deep moisture consumer." },
            "season_2": { "name": "Chickpea / Lentil", "season": "Post-Harvest Fallow (Feb - May)", "role": "Short duration pulse to replenish depleted nitrogen." },
            "season_3": { "name": "Millets / Pearl Millet (Bajra)", "season": "Pre-Monsoon", "role": "Low water consumer; restores soil microbial balance." },
            "benefits": ["Controls pink bollworm cycle", "Restores soil organic matter", "Reduces pesticide dependency"]
        }
    else:
        cycle = {
            "primary_crop": f"{crop_name.capitalize()}",
            "season_1": { "name": f"{crop_name.capitalize()}", "season": "Main Harvest Cycle", "role": "Primary cash crop production." },
            "season_2": { "name": "Mung Bean / Cowpea", "season": "Catch Crop (60 Days)", "role": "Fast-maturing pulse; fixes atmospheric nitrogen." },
            "season_3": { "name": "Cover Crop / Multigrain Grass", "season": "Off-season", "role": "Prevents soil erosion and organic matter loss." },
            "benefits": ["Maintains year-round canopy coverage", "Improves soil biodiversity", "Suppresses weed propagation"]
        }
        
    return {
        "success": True,
        "rotation_plan": cycle
    }

# ============================================================
# STATIC FILES MOUNTING & SPA FALLBACK
# ============================================================
if os.path.exists(CHARTS_CROP_DIR):
    app.mount("/charts/crop", StaticFiles(directory=CHARTS_CROP_DIR), name="charts_crop")
if os.path.exists(CHARTS_FERT_DIR):
    app.mount("/charts/fertilizer", StaticFiles(directory=CHARTS_FERT_DIR), name="charts_fert")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "Crop & Fertilizer ML Backend Running. Static index.html pending creation."})

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("[*] CROP & FERTILIZER ML PLATFORM RUNNING")
    print("[*] Open your browser at: http://localhost:8000")
    print("=" * 60 + "\n")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
