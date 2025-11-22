import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { ApiService } from './api.service';
import { LoginRequest, RegisterRequest, AuthResponse } from '../models/auth.model';
import { User } from '../models/user.model';
import { LoggerService } from './logger.service';

/**
 * Authentication service for managing user authentication and session
 */
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly TOKEN_KEY = 'access_token';
  private readonly USER_KEY = 'current_user';
  
  private currentUserSubject = new BehaviorSubject<User | null>(this.getStoredUser());
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(
    private apiService: ApiService,
    private logger: LoggerService
  ) {}

  /**
   * Login user
   */
  login(credentials: LoginRequest): Observable<AuthResponse> {
    return this.apiService.post<AuthResponse>('/auth/login', credentials).pipe(
      tap(response => {
        this.setToken(response.access_token);
        this.setUser(response.user);
        this.currentUserSubject.next(response.user);
        this.logger.info('User logged in:', response.user.email);
      })
    );
  }

  /**
   * Register new user
   */
  register(userData: RegisterRequest): Observable<AuthResponse> {
    return this.apiService.post<AuthResponse>('/auth/register', userData).pipe(
      tap(response => {
        this.setToken(response.access_token);
        this.setUser(response.user);
        this.currentUserSubject.next(response.user);
        this.logger.info('User registered:', response.user.email);
      })
    );
  }

  /**
   * Logout user
   */
  logout(): void {
    this.removeToken();
    this.removeUser();
    this.currentUserSubject.next(null);
    this.logger.info('User logged out');
  }

  /**
   * Get current user
   */
  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getToken() && !!this.getCurrentUser();
  }

  /**
   * Check if user has specific role
   */
  hasRole(role: string): boolean {
    const user = this.getCurrentUser();
    return user?.role === role;
  }

  /**
   * Get authentication token
   */
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Set authentication token
   */
  private setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  /**
   * Remove authentication token
   */
  private removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  /**
   * Get stored user from localStorage
   */
  private getStoredUser(): User | null {
    const userStr = localStorage.getItem(this.USER_KEY);
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  }

  /**
   * Set user in localStorage
   */
  private setUser(user: User): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
  }

  /**
   * Remove user from localStorage
   */
  private removeUser(): void {
    localStorage.removeItem(this.USER_KEY);
  }
}


