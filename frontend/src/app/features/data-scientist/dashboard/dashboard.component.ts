import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { RouterModule } from '@angular/router';

/**
 * Data Scientist dashboard component
 */
@Component({
  selector: 'app-data-scientist-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatIconModule,
    MatButtonModule,
    RouterModule
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DataScientistDashboardComponent implements OnInit {
  modelStats = [
    { label: 'Model Accuracy', value: 'N/A', icon: 'check_circle', color: 'primary' },
    { label: 'Total Predictions', value: '0', icon: 'psychology', color: 'accent' },
    { label: 'Model Version', value: '1.0.0', icon: 'science', color: 'warn' }
  ];

  ngOnInit(): void {
    // Load model metrics
  }
}
