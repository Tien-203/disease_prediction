import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil } from 'rxjs';
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
  per_disease_performance: Array<{
    disease: string;
    accuracy: number;
    precision: number;
    recall: number;
    f1_score?: number;
  }>;
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
  
  private destroy$ = new Subject<void>();

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadDataset();
  }

  ngOnDestroy(): void {
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
}

