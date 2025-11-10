import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

/**
 * HTTP Error Interceptor
 * Handles HTTP errors globally
 */
export const httpErrorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error: HttpErrorResponse | any) => {
      // Handle network errors (status 0 or undefined) and HTTP errors (status >= 400)
      // Don't intercept successful responses (status 200-299)
      
      // Network error or CORS error
      if (!error.status || error.status === 0) {
        const errorMessage = 'Network error. Please check if the backend server is running.';
        console.error('Network Error:', errorMessage, error);
        return throwError(() => ({ message: errorMessage, status: 0 }));
      }
      
      // HTTP error (status >= 400)
      if (error.status >= 400) {
        let errorMessage = 'An error occurred';

        if (error.error instanceof ErrorEvent) {
          // Client-side error
          errorMessage = `Error: ${error.error.message}`;
        } else {
          // Server-side error
          errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
          
          if (error.error?.detail) {
            errorMessage = error.error.detail;
          } else if (error.error?.message) {
            errorMessage = error.error.message;
          }
        }

        console.error('HTTP Error:', errorMessage);
        return throwError(() => ({ message: errorMessage, status: error.status }));
      }
      
      // Re-throw if it's not a recognized error type
      console.error('Unknown error type:', error);
      return throwError(() => error);
    })
  );
};

