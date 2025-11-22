import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { ErrorHandlerService } from '../services/error-handler.service';

/**
 * HTTP interceptor to handle errors globally
 */
export const httpErrorInterceptor: HttpInterceptorFn = (req, next) => {
  const errorHandler = inject(ErrorHandlerService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      const errorMessage = errorHandler.handleHttpError(error);
      return throwError(() => new Error(errorMessage));
    })
  );
};


