import { inject } from '@angular/core';
import { Router, CanActivateFn, ActivatedRouteSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { UserRole } from '../models/user.model';

/**
 * Guard to protect routes based on user role
 */
export const roleGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (!authService.isAuthenticated()) {
    router.navigate(['/auth/login']);
    return false;
  }

  const requiredRoles = route.data['roles'] as UserRole[];
  const user = authService.getCurrentUser();

  if (!requiredRoles || requiredRoles.length === 0) {
    return true;
  }

  if (user && requiredRoles.includes(user.role)) {
    return true;
  }

  // Redirect to unauthorized or home
  router.navigate(['/']);
  return false;
};


