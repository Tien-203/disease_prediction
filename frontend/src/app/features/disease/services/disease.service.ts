import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from '../../../core/services/api.service';

/**
 * Disease interface
 */
export interface DiseaseCreate {
  name: string;
  description?: string;
  severity?: string;
  precautions?: string[];
  recommendations?: string;
}

export interface DiseaseResponse {
  id: number;
  name: string;
  description?: string;
  severity?: string;
  precautions?: string[];
  recommendations?: string;
  created_at: string;
  updated_at: string;
}

export interface DiseaseListResponse {
  diseases: DiseaseResponse[];
  total: number;
}

/**
 * Symptom interface
 */
export interface SymptomCreate {
  name: string;
  description?: string;
}

export interface SymptomResponse {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

/**
 * Disease Service
 * Handles all disease-related API calls
 */
@Injectable({
  providedIn: 'root'
})
export class DiseaseService {
  constructor(private apiService: ApiService) {}

  /**
   * Create a new disease
   */
  createDisease(disease: DiseaseCreate): Observable<DiseaseResponse> {
    return this.apiService.post<DiseaseResponse>('/diseases', disease);
  }

  /**
   * Create a new symptom
   */
  createSymptom(symptom: SymptomCreate): Observable<SymptomResponse> {
    return this.apiService.post<SymptomResponse>('/symptoms', symptom);
  }

  /**
   * Search diseases by name
   */
  searchDiseases(name: string): Observable<DiseaseResponse[]> {
    return this.apiService.get<DiseaseListResponse>('/diseases/search', { name }).pipe(
      // Map to return just the diseases array
      map(response => response.diseases || [])
    );
  }
}


