/**
 * Disease model
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

