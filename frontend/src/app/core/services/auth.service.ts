import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, throwError, of } from 'rxjs';
import { tap, catchError, map } from 'rxjs/operators';
import { ApiService } from './api.service';
import { Router } from '@angular/router';
import { jwtDecode } from 'jwt-decode';

/**
 * Authentication Service
 * Handles user authentication and session management
 */
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly TOKEN_KEY = 'auth_token';
  private readonly USER_KEY = 'user_data';
  
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(this.hasToken());
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(
    private apiService: ApiService,
    private router: Router
  ) {
    // Auto-login for development/demo (bypass authentication)
    this.autoLogin();
  }

  /**
   * Auto-login as default user (for school project demo)
   */
  private autoLogin(): void {
    // Check if already authenticated
    if (this.hasToken()) {
      this.isAuthenticatedSubject.next(true);
      return;
    }

    // Create a mock session
    const mockUser = {
      id: 1,
      email: 'demo@patient.com',
      name: 'Demo Patient',
      role: 'patient',
      is_active: true,
      created_at: new Date().toISOString()
    };

    localStorage.setItem(this.TOKEN_KEY, 'mock-session-token');
    localStorage.setItem(this.USER_KEY, JSON.stringify(mockUser));
    this.isAuthenticatedSubject.next(true);

    console.log('Auto-login enabled with mock user:', mockUser);
  }

  /**
   * Check if user has a valid token
   */
  private hasToken(): boolean {
    return !!localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Login user
   */
  login(email: string, password: string, role?: string): Observable<any> {
    const payload: { email: string; password: string; role?: string } = { email, password };
    if (role) {
      payload.role = role;
    }

    return this.apiService.post('/auth/login', payload).pipe(
      map((response: any) => {
        console.log('Login response received:', response);
        try {
          // Ensure response is properly formatted
          if (response && typeof response === 'object') {
            this.handleAuthSuccess(response, { email, fallbackRole: role });
            return response;
          }
          throw new Error('Invalid response format');
        } catch (parseError: any) {
          console.error('Error parsing login response:', parseError);
          // If we have a valid response structure but parsing failed, still try to proceed
          if (response?.access_token || response?.token) {
            this.handleAuthSuccess(response, { email, fallbackRole: role });
            return response;
          }
          throw parseError;
        }
      }),
      catchError((error: any) => {
        console.error('Login error - full error object:', error);
        console.error('Login error - error.message:', error?.message);
        console.error('Login error - error.error:', error?.error);
        console.error('Login error - error.status:', error?.status);
        
        // Extract error message
        let errorMessage = 'Login failed. Please check your credentials.';
        
        if (error?.error?.detail) {
          errorMessage = error.error.detail;
        } else if (error?.error?.message) {
          errorMessage = error.error.message;
        } else if (error?.message) {
          errorMessage = error.message;
        }

        return throwError(() => ({ message: errorMessage }));
      })
    );
  }

  /**
   * Register new user
   */
  register(userData: { email: string; password: string; name?: string; age?: number; gender?: string; role?: string }): Observable<any> {
    const payload: {
      email: string;
      password: string;
      name?: string;
      age?: number;
      gender?: string;
      role?: string;
    } = {
      email: userData.email,
      password: userData.password
    };

    if (userData.name) {
      payload.name = userData.name;
    }
    if (typeof userData.age === 'number') {
      payload.age = userData.age;
    }
    if (userData.gender) {
      payload.gender = userData.gender;
    }
    if (userData.role) {
      payload.role = userData.role;
    }

    return this.apiService.post('/auth/register', payload).pipe(
      tap((response: any) => {
        this.handleAuthSuccess(response, { email: userData.email, fallbackRole: userData.role, fallbackName: userData.name });
      }),
      catchError((error: any) => {
        if (error.status === 200 || error.status === 0) {
          const syntheticResponse = this.handleAuthSuccess({}, { email: userData.email, fallbackRole: userData.role, fallbackName: userData.name });
          return of(syntheticResponse);
        }

        const errorMessage = error.error?.detail || error.error?.message || 'Registration failed. Please try again.';
        return throwError(() => ({ message: errorMessage }));
      })
    );
  }

  /**
   * Logout user
   */
  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    this.isAuthenticatedSubject.next(false);
    this.router.navigate(['/login']);
  }

  /**
   * Get current user
   */
  getCurrentUser(): any {
    const userData = localStorage.getItem(this.USER_KEY);
    return userData ? JSON.parse(userData) : null;
  }

  /**
   * Get authentication token
   */
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return this.isAuthenticatedSubject.value;
  }

  /**
   * Get user role from token or localStorage
   */
  getUserRole(): string | null {
    const user = this.getCurrentUser();
    if (user && user.role) {
      return user.role.toLowerCase();
    }

    // Try to decode token as fallback
    const token = this.getToken();
    if (token && token !== 'session') {
      try {
        const decoded: any = jwtDecode(token);
        return decoded.role ? decoded.role.toLowerCase() : null;
      } catch (error) {
        console.error('Error decoding token:', error);
        return null;
      }
    }

    return null;
  }

  /**
   * Check if user has a specific role
   */
  hasRole(role: string): boolean {
    const userRole = this.getUserRole();
    return userRole === role.toLowerCase();
  }

  /**
   * Check if user has any of the specified roles
   */
  hasAnyRole(roles: string[]): boolean {
    const userRole = this.getUserRole();
    return roles.some(role => role.toLowerCase() === userRole);
  }

  private handleAuthSuccess(
    response: any,
    options: { email: string; fallbackRole?: string; fallbackName?: string }
  ) {
    const { email, fallbackRole, fallbackName } = options;
    
    console.log('Handling auth success, response:', response);
    
    // Extract access token from response
    const tokenValue: string =
      (response && (response.access_token || response.token)) || 'session';
    
    if (!tokenValue || tokenValue === 'session') {
      console.warn('No access token found in response');
    }
    
    localStorage.setItem(this.TOKEN_KEY, tokenValue);

    const selectedRole = (fallbackRole || 'patient').toLowerCase();
    const normalizedRole = (response?.user?.role || selectedRole).toLowerCase();

    if (response?.user) {
      // Handle datetime serialization - convert to ISO string if needed
      const userData: any = {
        id: response.user.id,
        email: response.user.email,
        name: response.user.name,
        age: response.user.age,
        gender: response.user.gender,
        role: normalizedRole,
        is_active: response.user.is_active
      };
      
      // Convert datetime objects to ISO strings for localStorage
      if (response.user.created_at) {
        userData.created_at = typeof response.user.created_at === 'string' 
          ? response.user.created_at 
          : new Date(response.user.created_at).toISOString();
      }
      if (response.user.updated_at) {
        userData.updated_at = typeof response.user.updated_at === 'string'
          ? response.user.updated_at
          : new Date(response.user.updated_at).toISOString();
      }
      if (response.user.last_login) {
        userData.last_login = typeof response.user.last_login === 'string'
          ? response.user.last_login
          : new Date(response.user.last_login).toISOString();
      }
      
      localStorage.setItem(this.USER_KEY, JSON.stringify(userData));
      console.log('User data saved to localStorage:', userData);
    } else {
      const fallbackUser = {
        email,
        name: fallbackName || email.split('@')[0],
        role: normalizedRole
      };
      localStorage.setItem(this.USER_KEY, JSON.stringify(fallbackUser));
      console.log('Fallback user data saved:', fallbackUser);
    }

    this.isAuthenticatedSubject.next(true);
    console.log('Authentication state updated to true');
    
    return response || { access_token: tokenValue, user: this.getCurrentUser() };
  }
}

