import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../core/services/api.service';
import { HttpParams } from '@angular/common/http';

/**
 * Disease interface matching backend schema
 */
export interface Disease {
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
  diseases: Disease[];
  total: number;
}

/**
 * Disease service for managing diseases
 */
@Injectable({
  providedIn: 'root'
})
export class DiseaseService {
  constructor(private apiService: ApiService) {}

  /**
   * Get all diseases with pagination
   */
  getDiseases(skip: number = 0, limit: number = 100): Observable<DiseaseListResponse> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.apiService.get<DiseaseListResponse>('/diseases', params);
  }

  /**
   * Get disease by ID
   */
  getDiseaseById(id: number): Observable<Disease> {
    return this.apiService.get<Disease>(`/diseases/${id}`);
  }

  /**
   * Search diseases by name
   */
  searchDiseases(name: string): Observable<DiseaseListResponse> {
    const params = new HttpParams().set('name', name);
    return this.apiService.get<DiseaseListResponse>('/diseases/search', params);
  }

  /**
   * Create new disease (admin only)
   */
  createDisease(disease: {
    name: string;
    description?: string;
    severity?: string;
    precautions?: string[];
    recommendations?: string;
  }): Observable<Disease> {
    return this.apiService.post<Disease>('/diseases', disease);
  }

  /**
   * Update disease (admin only)
   */
  updateDisease(id: number, disease: {
    name?: string;
    description?: string;
    severity?: string;
    precautions?: string[];
    recommendations?: string;
  }): Observable<Disease> {
    return this.apiService.put<Disease>(`/diseases/${id}`, disease);
  }

  /**
   * Delete disease (admin only)
   */
  deleteDisease(id: number): Observable<void> {
    return this.apiService.delete<void>(`/diseases/${id}`);
  }
}


