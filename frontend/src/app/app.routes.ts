import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { LoginComponent } from './features/auth/login/login.component';
import { RegisterComponent } from './features/auth/register/register.component';
import { HistoryComponent } from './features/history/history.component';
import { ProfileComponent } from './features/profile/profile.component';
import { PredictionComponent } from './features/prediction/prediction.component';
import { AboutComponent } from './features/about/about.component';
import { DataScientistDashboardComponent } from './features/data-scientist/datascientist-dashboard.component';
import { DataScientistProfileComponent } from './features/data-scientist/datascientist-profile.component';
import { DataScientistDatasetComponent } from './features/data-scientist/datascientist-dataset.component';
import { DoctorDashboardComponent } from './features/doctor/doctor-dashboard.component';
import { DoctorProfileComponent } from './features/doctor/doctor-profile.component';
import { DoctorDatasetComponent } from './features/doctor/doctor-dataset.component';
import { DoctorPatientsComponent } from './features/doctor/doctor-patients.component';
import { ResearcherDashboardComponent } from './features/researcher/researcher-dashboard.component';
import { ResearcherProfileComponent } from './features/researcher/researcher-profile.component';
import { ResearcherDatasetComponent } from './features/researcher/researcher-dataset.component';

/**
 * Application routes
 */
export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'patient'
  },
  {
    path: 'patient',
    component: HomeComponent,
    title: 'Patient Home - Disease Prediction'
  },
  {
    path: 'researcher',
    component: ResearcherDashboardComponent,
    title: 'Researcher Home - Disease Prediction'
  },
  {
    path: 'researcher/profile',
    component: ResearcherProfileComponent,
    title: 'Researcher Profile - Disease Prediction'
  },
  {
    path: 'researcher/dataset',
    component: ResearcherDatasetComponent,
    title: 'Researcher Dataset - Disease Prediction'
  },
  {
    path: 'doctor',
    component: DoctorDashboardComponent,
    title: 'Doctor Home - Disease Prediction'
  },
  {
    path: 'doctor/profile',
    component: DoctorProfileComponent,
    title: 'Doctor Profile - Disease Prediction'
  },
  {
    path: 'doctor/dataset',
    component: DoctorDatasetComponent,
    title: 'Doctor Dataset - Disease Prediction'
  },
  {
    path: 'doctor/patients',
    component: DoctorPatientsComponent,
    title: 'Patients - Disease Prediction'
  },
  {
    path: 'ds',
    component: DataScientistDashboardComponent,
    title: 'Data Scientist Home - Disease Prediction'
  },
  {
    path: 'ds/profile',
    component: DataScientistProfileComponent,
    title: 'Data Scientist Profile - Disease Prediction'
  },
  {
    path: 'ds/dataset',
    component: DataScientistDatasetComponent,
    title: 'Dataset - Disease Prediction'
  },
  {
    path: 'profile',
    component: ProfileComponent,
    title: 'Profile - Disease Prediction'
  },
  {
    path: 'history',
    component: HistoryComponent,
    title: 'History - Disease Prediction'
  },
  {
    path: 'login',
    component: LoginComponent,
    title: 'Login - Disease Prediction'
  },
  {
    path: 'register',
    component: RegisterComponent,
    title: 'Register - Disease Prediction'
  },
  {
    path: 'prediction',
    component: PredictionComponent,
    title: 'Prediction - Disease Prediction'
  },
  {
    path: 'about',
    component: AboutComponent,
    title: 'About - Disease Prediction'
  },
  {
    path: '**',
    redirectTo: 'patient'
  }
];

