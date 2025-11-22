/**
 * User model matching backend schema
 */
export interface User {
  id: number;
  email: string;
  name?: string;
  age?: number;
  gender?: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  last_login?: string;
}

export type UserRole = 'patient' | 'doctor' | 'researcher' | 'data_scientist';


