import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../core/services/api.service';
import { HttpParams } from '@angular/common/http';

/**
 * Prediction interfaces matching backend schema
 */
export interface PredictionRequest {
  symptoms: string[];
  session_id?: string;
}

export interface AlternativePrediction {
  disease: string;
  confidence: number;
}

export interface PredictionResponse {
  predicted_disease: string;
  confidence: number;
  alternatives: AlternativePrediction[];
  symptoms_used: string[];
  disease_info?: any;
}

export interface PredictionHistory {
  id: number;
  symptoms: string[];
  predicted_disease: string;
  confidence: number;
  timestamp: string;
  session_id?: string;
}

export interface PredictionHistoryListResponse {
  predictions: PredictionHistory[];
  total: number;
}

/**
 * Prediction service for disease predictions
 */
@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  constructor(private apiService: ApiService) {}

  /**
   * Make disease prediction based on symptoms
   */
  predict(request: PredictionRequest): Observable<PredictionResponse> {
    return this.apiService.post<PredictionResponse>('/predict', request);
  }

  /**
   * Get prediction history
   */
  getHistory(skip: number = 0, limit: number = 100, sessionId?: string): Observable<PredictionHistoryListResponse> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    
    if (sessionId) {
      params = params.set('session_id', sessionId);
    }
    
    return this.apiService.get<PredictionHistoryListResponse>('/predict/history', params);
  }

  /**
   * Get specific prediction by ID
   */
  getPredictionById(id: number): Observable<PredictionHistory> {
    return this.apiService.get<PredictionHistory>(`/predict/${id}`);
  }
}


