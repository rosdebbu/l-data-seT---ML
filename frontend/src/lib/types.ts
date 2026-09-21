export interface CropInput {
  N: number;
  P: number;
  K: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
}

export interface CropPredictionResponse {
  prediction: string;
  scientific_name: string;
  category: string;
  season: string;
  rationale: string;
  model: string;
  score: number;
  consensus: {
    random_forest: string;
    decision_tree: string;
    knn: string;
  };
}

export interface FertilizerInput {
  soil_type: string;
  crop_type: string;
  moisture: number;
  temperature: number;
  humidity: number;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
}

export interface FertilizerPredictionResponse {
  prediction: string;
  chemical_formula: string;
  npk_ratio: string;
  soil_type: string;
  crop_type: string;
  primary_role: string;
  application_guidance: string;
  soil_health_warning: string;
  model: string;
  score: number;
}

export interface ModelMetrics {
  rf_accuracy: number;
  dt_accuracy: number;
  knn_accuracy: number;
  rf_f1: number;
  dataset_size: number;
}
