import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { finalize } from 'rxjs';
import { LoadingService } from '../services/loading.service';

/**
 * HTTP interceptor to show loading indicators
 */
export const loadingInterceptor: HttpInterceptorFn = (req, next) => {
  const loadingService = inject(LoadingService);

  // Show loading for non-GET requests or specific endpoints
  if (req.method !== 'GET' || req.url.includes('/predict')) {
    loadingService.show();
  }

  return next(req).pipe(
    finalize(() => {
      loadingService.hide();
    })
  );
};


