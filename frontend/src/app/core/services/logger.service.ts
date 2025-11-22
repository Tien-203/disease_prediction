import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

/**
 * Logging service for application-wide logging
 */
@Injectable({
  providedIn: 'root'
})
export class LoggerService {
  /**
   * Log info message
   */
  info(message: string, ...args: any[]): void {
    console.log(`[INFO] ${message}`, ...args);
  }

  /**
   * Log warning message
   */
  warn(message: string, ...args: any[]): void {
    console.warn(`[WARN] ${message}`, ...args);
  }

  /**
   * Log error message
   */
  error(message: string, ...args: any[]): void {
    console.error(`[ERROR] ${message}`, ...args);
  }

  /**
   * Log debug message
   */
  debug(message: string, ...args: any[]): void {
    if (!environment.production) {
      console.debug(`[DEBUG] ${message}`, ...args);
    }
  }
}
