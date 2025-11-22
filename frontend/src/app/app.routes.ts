import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';
import { UserRole } from './core/models/user.model';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./features/home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.routes').then(m => m.authRoutes)
  },
  {
    path: 'patient',
    canActivate: [authGuard, roleGuard],
    data: { roles: ['patient'] },
    children: [
      {
        path: 'predict',
        loadComponent: () => import('./features/patient/prediction/prediction.component').then(m => m.PredictionComponent)
      },
      {
        path: 'history',
        loadComponent: () => import('./features/patient/history/history.component').then(m => m.HistoryComponent)
      },
      {
        path: '',
        redirectTo: 'predict',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: 'doctor',
    canActivate: [authGuard, roleGuard],
    data: { roles: ['doctor'] },
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./features/doctor/dashboard/dashboard.component').then(m => m.DoctorDashboardComponent)
      },
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: 'data-scientist',
    canActivate: [authGuard, roleGuard],
    data: { roles: ['data_scientist'] },
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./features/data-scientist/dashboard/dashboard.component').then(m => m.DataScientistDashboardComponent)
      },
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: 'researcher',
    canActivate: [authGuard, roleGuard],
    data: { roles: ['researcher'] },
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./features/researcher/dashboard/dashboard.component').then(m => m.ResearcherDashboardComponent)
      },
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: '**',
    redirectTo: '',
    pathMatch: 'full'
  }
];
