import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PredictionService } from './services/prediction.service';
import { PredictionRequest, PredictionResponse } from './models/prediction.model';
import { Symptom } from './models/symptom.model';

/**
 * Prediction Component
 * Main component for disease prediction
 */
@Component({
  selector: 'app-prediction',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.scss']
})
export class PredictionComponent implements OnInit {
  // Form fields
  patientName: string = '';
  patientAge: number | null = null;
  
  // Symptoms
  availableSymptoms: Symptom[] = [];
  selectedSymptoms: Set<string> = new Set();
  searchTerm: string = '';
  
  // Prediction result
  predictionResult: PredictionResponse | null = null;
  
  // UI state
  loading: boolean = false;
  error: string | null = null;
  symptomsLoading: boolean = false;

  constructor(private predictionService: PredictionService) {}

  ngOnInit() {
    this.loadSymptoms();
  }

  /**
   * Load available symptoms from API
   */
  loadSymptoms() {
    this.symptomsLoading = true;
    this.predictionService.getSymptoms().subscribe({
      next: (response) => {
        this.availableSymptoms = response.symptoms;
        this.symptomsLoading = false;
      },
      error: (err) => {
        this.error = 'Failed to load symptoms. Please try again.';
        this.symptomsLoading = false;
        console.error('Error loading symptoms:', err);
      }
    });
  }

  /**
   * Get filtered symptoms based on search term
   */
  get filteredSymptoms(): Symptom[] {
    if (!this.searchTerm) {
      return this.availableSymptoms;
    }
    
    const search = this.searchTerm.toLowerCase();
    return this.availableSymptoms.filter(symptom =>
      symptom.name.toLowerCase().includes(search) ||
      symptom.description?.toLowerCase().includes(search)
    );
  }

  /**
   * Toggle symptom selection
   */
  toggleSymptom(symptomName: string) {
    if (this.selectedSymptoms.has(symptomName)) {
      this.selectedSymptoms.delete(symptomName);
    } else {
      this.selectedSymptoms.add(symptomName);
    }
  }

  /**
   * Check if symptom is selected
   */
  isSymptomSelected(symptomName: string): boolean {
    return this.selectedSymptoms.has(symptomName);
  }

  /**
   * Submit prediction request
   */
  submitPrediction() {
    // Validation
    if (this.selectedSymptoms.size === 0) {
      this.error = 'Please select at least one symptom';
      return;
    }

    this.loading = true;
    this.error = null;
    this.predictionResult = null;

    const request: PredictionRequest = {
      symptoms: Array.from(this.selectedSymptoms)
    };

    this.predictionService.predictDisease(request).subscribe({
      next: (response) => {
        this.predictionResult = response;
        this.loading = false;
        // Scroll to results
        setTimeout(() => {
          document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      },
      error: (err) => {
        this.error = err.message || 'Failed to get prediction. Please try again.';
        this.loading = false;
        console.error('Prediction error:', err);
      }
    });
  }

  /**
   * Reset form and results
   */
  resetForm() {
    this.patientName = '';
    this.patientAge = null;
    this.selectedSymptoms.clear();
    this.predictionResult = null;
    this.error = null;
    this.searchTerm = '';
  }

  /**
   * Get confidence percentage
   */
  getConfidencePercentage(confidence: number): number {
    return Math.round(confidence * 100);
  }

  /**
   * Get severity color class
   */
  getSeverityClass(severity?: string): string {
    switch (severity?.toLowerCase()) {
      case 'mild':
        return 'severity-mild';
      case 'moderate':
        return 'severity-moderate';
      case 'severe':
        return 'severity-severe';
      default:
        return '';
    }
  }
}

