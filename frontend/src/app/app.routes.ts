import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { PredictionComponent } from './features/prediction/prediction.component';

/**
 * Application routes
 */
export const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
    title: 'Home - Disease Prediction'
  },
  {
    path: 'prediction',
    component: PredictionComponent,
    title: 'Prediction - Disease Prediction'
  },
  {
    path: '**',
    redirectTo: ''
  }
];

