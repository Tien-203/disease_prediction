import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { RouterModule } from '@angular/router';

/**
 * Doctor dashboard component
 */
@Component({
  selector: 'app-doctor-dashboard',
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
export class DoctorDashboardComponent implements OnInit {
  stats = [
    { label: 'Total Patients', value: '0', icon: 'people', color: 'primary' },
    { label: 'Predictions Today', value: '0', icon: 'psychology', color: 'accent' },
    { label: 'Active Cases', value: '0', icon: 'local_hospital', color: 'warn' }
  ];

  ngOnInit(): void {
    // Load doctor dashboard data
  }
}
