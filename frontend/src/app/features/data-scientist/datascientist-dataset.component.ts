import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil, interval } from 'rxjs';
import { ApiService } from '../../core/services/api.service';

interface DatasetRecord {
  date_modified: string;
  disease: string;
  symptoms: string[];
}

interface ModelPerformance {
  model_type: string;
  model_version: string;
  n_estimators?: number;
  n_features: number;
  n_classes: number;
  overall_metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
    accuracy_std?: number;
    precision_std?: number;
    recall_std?: number;
    f1_std?: number;
  };
}

interface RetrainResponse {
  message: string;
  status: string;
}

/**
 * Data Scientist dataset component
 */
@Component({
  selector: 'app-datascientist-dataset',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './datascientist-dataset.component.html',
  styleUrls: ['./datascientist-dataset.component.scss']
})
export class DataScientistDatasetComponent implements OnInit, OnDestroy {
  searchTerm = '';
  records: DatasetRecord[] = [];
  isLoading = false;
  performanceModalOpen = false;
  modelPerformance: ModelPerformance | null = null;
  isLoadingPerformance = false;
  isRetraining = false;
  retrainMessage = '';
  retrainError = '';
  trainingStatus: 'idle' | 'training' | 'completed' | 'failed' = 'idle';
  private pollingInterval?: any;
  
  private destroy$ = new Subject<void>();

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadDataset();
  }

  ngOnDestroy(): void {
    this.stopPolling();
    this.destroy$.next();
    this.destroy$.complete();
  }

  get filteredRecords(): DatasetRecord[] {
    const term = this.searchTerm.trim().toLowerCase();
    if (!term) {
      return this.records;
    }
    return this.records.filter((record) =>
      record.disease.toLowerCase().includes(term) ||
      record.symptoms.some(symptom => symptom.toLowerCase().includes(term))
    );
  }

  loadDataset(): void {
    this.isLoading = true;
    this.apiService.get<{ records: DatasetRecord[]; total: number }>('/dataset/records')
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response: { records: DatasetRecord[]; total: number }) => {
          this.records = response.records;
          this.isLoading = false;
        },
        error: (error: any) => {
          console.error('Error loading dataset:', error);
          this.isLoading = false;
        }
      });
  }

  refreshDataset(): void {
    this.loadDataset();
  }

  openPerformanceModal(): void {
    this.performanceModalOpen = true;
    this.loadModelPerformance();
  }

  closePerformanceModal(): void {
    this.performanceModalOpen = false;
  }

  loadModelPerformance(): void {
    this.isLoadingPerformance = true;
    this.apiService.get<ModelPerformance>('/model/performance')
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (performance: ModelPerformance) => {
          this.modelPerformance = performance;
          this.isLoadingPerformance = false;
        },
        error: (error: any) => {
          console.error('Error loading model performance:', error);
          this.isLoadingPerformance = false;
        }
      });
  }

  formatPercentage(value: number): string {
    return `${(value * 100).toFixed(1)}%`;
  }

  retrainModel(): void {
    if (this.isRetraining) {
      return;
    }

    if (!confirm('Are you sure you want to retrain the model? This may take several minutes.')) {
      return;
    }

    this.isRetraining = true;
    this.retrainMessage = '';
    this.retrainError = '';
    this.trainingStatus = 'training';

    this.apiService.post<RetrainResponse>('/model/retrain', {})
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response: RetrainResponse) => {
          this.retrainMessage = response.message;
          // Start polling for training status
          this.startPolling();
        },
        error: (error: any) => {
          console.error('Error retraining model:', error);
          this.retrainError = error?.error?.detail || error?.message || 'Failed to start model retraining. Please try again.';
          this.isRetraining = false;
          this.trainingStatus = 'failed';
        }
      });
  }

  startPolling(): void {
    // Poll every 5 seconds
    this.pollingInterval = interval(5000)
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        this.checkTrainingStatus();
      });
    
    // Check immediately
    this.checkTrainingStatus();
  }

  stopPolling(): void {
    if (this.pollingInterval) {
      this.pollingInterval.unsubscribe();
      this.pollingInterval = undefined;
    }
  }

  checkTrainingStatus(): void {
    this.apiService.get<{
      is_training: boolean;
      status: string;
      message: string;
      started_at: string | null;
      completed_at: string | null;
      error: string | null;
    }>('/model/training-status')
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (status) => {
          this.trainingStatus = status.status as 'idle' | 'training' | 'completed' | 'failed';
          this.retrainMessage = status.message;
          
          if (status.status === 'completed') {
            this.isRetraining = false;
            this.stopPolling();
            // Reload performance metrics
            if (this.performanceModalOpen) {
              this.loadModelPerformance();
            }
            // Reload dataset
            this.loadDataset();
          } else if (status.status === 'failed') {
            this.isRetraining = false;
            this.retrainError = status.error || 'Model training failed';
            this.stopPolling();
          } else if (status.status === 'training') {
            this.isRetraining = true;
          } else {
            this.isRetraining = false;
            this.stopPolling();
          }
        },
        error: (error: any) => {
          console.error('Error checking training status:', error);
          // Continue polling even if there's an error
        }
      });
  }
}

