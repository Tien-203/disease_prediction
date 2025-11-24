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

/**
 * Symptom option in a group
 */
export interface SymptomOption {
  id: number;
  name: string;
  display_name: string;
}

/**
 * Symptom group (question with options)
 */
export interface SymptomGroup {
  id: string;
  question: string;
  options: SymptomOption[];
  allow_multiple: boolean;
}

/**
 * Symptom groups response
 */
export interface SymptomGroupsResponse {
  groups: SymptomGroup[];
}

