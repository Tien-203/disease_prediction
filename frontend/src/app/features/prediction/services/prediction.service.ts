import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';
import {
  PredictionRequest,
  PredictionResponse,
  PredictionHistory
} from '../models/prediction.model';
import { SymptomListResponse } from '../models/symptom.model';

/**
 * Prediction Service
 * Handles all prediction-related API calls
 */
@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  constructor(private apiService: ApiService) {}

  /**
   * Get all available symptoms
   */
  getSymptoms(skip: number = 0, limit: number = 100): Observable<SymptomListResponse> {
    return this.apiService.get<SymptomListResponse>('/symptoms', { skip, limit });
  }

  /**
   * Predict disease based on symptoms
   */
  predictDisease(request: PredictionRequest): Observable<PredictionResponse> {
    return this.apiService.post<PredictionResponse>('/predict', request);
  }

  /**
   * Get prediction history
   */
  getPredictionHistory(skip: number = 0, limit: number = 10): Observable<any> {
    return this.apiService.get('/predict/history', { skip, limit });
  }

  /**
   * Check API health
   */
  checkHealth(): Observable<any> {
    return this.apiService.get('/health');
  }
}

