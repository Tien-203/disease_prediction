import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Disease } from '../../../features/services/disease.service';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';

/**
 * Disease card component to display disease information
 */
@Component({
  selector: 'app-disease-card',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatChipsModule,
    MatIconModule
  ],
  templateUrl: './disease-card.component.html',
  styleUrl: './disease-card.component.scss'
})
export class DiseaseCardComponent {
  @Input() disease!: Disease;

  /**
   * Get severity color
   */
  getSeverityColor(severity?: string): string {
    switch (severity?.toLowerCase()) {
      case 'mild':
        return 'primary';
      case 'moderate':
        return 'accent';
      case 'severe':
        return 'warn';
      default:
        return '';
    }
  }
}
