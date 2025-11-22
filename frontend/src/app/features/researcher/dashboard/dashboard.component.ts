import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { RouterModule } from '@angular/router';

/**
 * Researcher dashboard component
 */
@Component({
  selector: 'app-researcher-dashboard',
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
export class ResearcherDashboardComponent implements OnInit {
  researchStats = [
    { label: 'Total Diseases', value: '0', icon: 'local_hospital', color: 'primary' },
    { label: 'Total Symptoms', value: '0', icon: 'healing', color: 'accent' },
    { label: 'Research Data Points', value: '0', icon: 'data_usage', color: 'warn' }
  ];

  ngOnInit(): void {
    // Load research data
  }
}
