import { ApplicationConfig } from '@angular/core';
import { provideRouter, withComponentInputBinding, withDebugTracing } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { routes } from './app.routes';
import { httpErrorInterceptor } from './core/interceptors/http-error.interceptor';

/**
 * Application configuration
 */
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(
      routes,
      // Uncomment withDebugTracing() below to enable router tracing for debugging
      // withDebugTracing(),
      withComponentInputBinding() // Enable component input binding from route params
    ),
    provideHttpClient(
      withInterceptors([httpErrorInterceptor])
    )
  ]
};

