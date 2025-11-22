import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PredictionService, PredictionResponse } from '../../services/prediction.service';
import { DiseaseService } from '../../services/disease.service';
import { SymptomSelectorComponent } from '../../../shared/components/symptom-selector/symptom-selector.component';
import { PredictionResultComponent } from '../../../shared/components/prediction-result/prediction-result.component';
import { DiseaseCardComponent } from '../../../shared/components/disease-card/disease-card.component';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ErrorHandlerService } from '../../../core/services/error-handler.service';
import { LoggerService } from '../../../core/services/logger.service';

/**
 * Patient prediction component
 */
@Component({
  selector: 'app-prediction',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    SymptomSelectorComponent,
    PredictionResultComponent,
    DiseaseCardComponent
  ],
  templateUrl: './prediction.component.html',
  styleUrl: './prediction.component.scss'
})
export class PredictionComponent implements OnInit {
  selectedSymptoms: string[] = [];
  predictionResult: PredictionResponse | null = null;
  diseaseInfo: any = null;
  errorMessage = '';
  isLoading = false;

  constructor(
    private predictionService: PredictionService,
    private diseaseService: DiseaseService,
    private errorHandler: ErrorHandlerService,
    private logger: LoggerService
  ) {}

  ngOnInit(): void {
    // Component initialization
  }

  /**
   * Handle symptom selection change
   */
  onSymptomsChange(symptoms: string[]): void {
    this.selectedSymptoms = symptoms;
  }

  /**
   * Make prediction
   */
  makePrediction(): void {
    if (this.selectedSymptoms.length === 0) {
      this.errorMessage = 'Please select at least one symptom';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.predictionResult = null;
    this.diseaseInfo = null;

    const request = {
      symptoms: this.selectedSymptoms,
      session_id: this.generateSessionId()
    };

    this.predictionService.predict(request).subscribe({
      next: (response) => {
        this.predictionResult = response;
        this.logger.info('Prediction successful:', response.predicted_disease);
        
        // Load disease information if available
        if (response.disease_info) {
          this.diseaseInfo = response.disease_info;
        } else {
          this.loadDiseaseInfo(response.predicted_disease);
        }
        
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = this.errorHandler.handleError(error);
        this.isLoading = false;
      }
    });
  }

  /**
   * Load disease information
   */
  private loadDiseaseInfo(diseaseName: string): void {
    this.diseaseService.searchDiseases(diseaseName).subscribe({
      next: (response) => {
        if (response.diseases && response.diseases.length > 0) {
          this.diseaseInfo = response.diseases[0];
        }
      },
      error: (error) => {
        this.logger.warn('Could not load disease info:', error);
      }
    });
  }

  /**
   * Generate session ID
   */
  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Reset form
   */
  reset(): void {
    this.selectedSymptoms = [];
    this.predictionResult = null;
    this.diseaseInfo = null;
    this.errorMessage = '';
  }
}
