import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../core/services/api.service';
import { HttpParams } from '@angular/common/http';

/**
 * Symptom interface matching backend schema
 */
export interface Symptom {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface SymptomListResponse {
  symptoms: Symptom[];
  total: number;
}

/**
 * Symptom service for managing symptoms
 */
@Injectable({
  providedIn: 'root'
})
export class SymptomService {
  constructor(private apiService: ApiService) {}

  /**
   * Get all symptoms with pagination
   */
  getSymptoms(skip: number = 0, limit: number = 100): Observable<SymptomListResponse> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.apiService.get<SymptomListResponse>('/symptoms', params);
  }

  /**
   * Get symptom by ID
   */
  getSymptomById(id: number): Observable<Symptom> {
    return this.apiService.get<Symptom>(`/symptoms/${id}`);
  }

  /**
   * Create new symptom (admin only)
   */
  createSymptom(symptom: { name: string; description?: string }): Observable<Symptom> {
    return this.apiService.post<Symptom>('/symptoms', symptom);
  }

  /**
   * Update symptom (admin only)
   */
  updateSymptom(id: number, symptom: { name?: string; description?: string }): Observable<Symptom> {
    return this.apiService.put<Symptom>(`/symptoms/${id}`, symptom);
  }

  /**
   * Delete symptom (admin only)
   */
  deleteSymptom(id: number): Observable<void> {
    return this.apiService.delete<void>(`/symptoms/${id}`);
  }
}


