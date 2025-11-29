/**
 * Prediction models
 */
export interface PredictionRequest {
  symptoms: string[];
  session_id?: string;
}

export interface AlternativePrediction {
  disease: string;
  confidence: number;
}

export interface DiseaseInfo {
  description?: string;
  severity?: string;
  precautions?: string[];
  recommendations?: string;
}

export interface PredictionResponse {
  predicted_disease: string;
  confidence: number;
  alternatives: AlternativePrediction[];
  symptoms_used: string[];
  disease_info?: DiseaseInfo;
}

export interface PredictionHistory {
  id: number;
  symptoms: string[];
  predicted_disease: string;
  confidence: number;
  timestamp: string;
  session_id?: string;
  corrected_disease?: string;
}

export interface PatientPrediction {
  id: number;
  user_id?: number;
  user_name?: string;
  user_age?: number;
  user_gender?: string;
  symptoms: string[];
  predicted_disease: string;
  confidence: number;
  timestamp: string;
  corrected_disease?: string;
  recommendation?: string;
}

export interface PredictionUpdateRequest {
  corrected_disease: string;
}

