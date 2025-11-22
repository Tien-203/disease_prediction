import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

/**
 * Home/Landing page component
 */
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  features = [
    {
      icon: 'psychology',
      title: 'AI-Powered Predictions',
      description: 'Get accurate disease predictions using advanced machine learning algorithms'
    },
    {
      icon: 'search',
      title: 'Symptom Analysis',
      description: 'Select your symptoms and receive instant predictions with confidence scores'
    },
    {
      icon: 'history',
      title: 'Prediction History',
      description: 'Track your prediction history and monitor your health over time'
    },
    {
      icon: 'local_hospital',
      title: 'Disease Information',
      description: 'Access detailed information about diseases, precautions, and recommendations'
    }
  ];
}
