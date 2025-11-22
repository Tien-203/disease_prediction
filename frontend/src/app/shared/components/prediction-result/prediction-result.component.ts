import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PredictionResponse } from '../../../features/services/prediction.service';
import { ConfidencePipe } from '../../pipes/confidence.pipe';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';

/**
 * Prediction result component to display prediction results
 */
@Component({
  selector: 'app-prediction-result',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatChipsModule,
    MatIconModule,
    MatProgressBarModule,
    ConfidencePipe
  ],
  templateUrl: './prediction-result.component.html',
  styleUrl: './prediction-result.component.scss'
})
export class PredictionResultComponent {
  @Input() prediction!: PredictionResponse;

  /**
   * Get confidence color based on value
   */
  getConfidenceColor(confidence: number): string {
    if (confidence >= 0.8) return 'primary';
    if (confidence >= 0.6) return 'accent';
    return 'warn';
  }
}
