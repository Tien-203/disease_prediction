import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { LoggerService } from './logger.service';

/**
 * Global error handler service
 */
@Injectable({
  providedIn: 'root'
})
export class ErrorHandlerService {
  constructor(private logger: LoggerService) {}

  /**
   * Handle HTTP error
   */
  handleHttpError(error: HttpErrorResponse): string {
    let errorMessage = 'An unexpected error occurred';

    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      if (error.error?.detail) {
        errorMessage = error.error.detail;
      } else if (error.error?.message) {
        errorMessage = error.error.message;
      } else {
        errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
      }
    }

    this.logger.error('HTTP Error:', errorMessage);
    return errorMessage;
  }

  /**
   * Handle generic error
   */
  handleError(error: any): string {
    const errorMessage = error?.message || 'An unexpected error occurred';
    this.logger.error('Error:', errorMessage);
    return errorMessage;
  }
}


