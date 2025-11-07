/**
 * Symptom model
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

