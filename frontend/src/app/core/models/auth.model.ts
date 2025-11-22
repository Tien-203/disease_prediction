import { User, UserRole } from './user.model';

/**
 * Authentication request/response interfaces
 */
export interface LoginRequest {
  email: string;
  password: string;
  role?: UserRole;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name?: string;
  age?: number;
  gender?: string;
  role?: UserRole;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface TokenData {
  sub?: string;
  user_id?: number;
  exp?: number;
}


