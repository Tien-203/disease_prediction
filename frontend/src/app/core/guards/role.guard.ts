import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

/**
 * Role Guard Factory
 * Creates guards for specific roles
 */
export function roleGuard(allowedRoles: string[]): CanActivateFn {
  return (route, state) => {
    const authService = inject(AuthService);
    const router = inject(Router);

    if (!authService.isAuthenticated()) {
      router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
      return false;
    }

    const userRole = authService.getUserRole();
    const hasAccess = userRole && allowedRoles.some(role => role.toLowerCase() === userRole);

    if (!hasAccess) {
      // Redirect to user's dashboard based on their role
      switch (userRole) {
        case 'patient':
          router.navigate(['/patient/home']);
          break;
        case 'doctor':
          router.navigate(['/doctor/dashboard']);
          break;
        case 'data scientist':
        case 'datascientist':
          router.navigate(['/data-scientist/dashboard']);
          break;
        case 'researcher':
          router.navigate(['/researcher/dashboard']);
          break;
        default:
          router.navigate(['/login']);
      }
      return false;
    }

    return true;
  };
}

// Specific role guards
export const patientGuard = roleGuard(['patient']);
export const doctorGuard = roleGuard(['doctor']);
export const dataScientistGuard = roleGuard(['data scientist', 'datascientist']);
export const researcherGuard = roleGuard(['researcher']);






