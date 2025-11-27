import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { forkJoin } from 'rxjs';
import { PredictionService } from '../prediction/services/prediction.service';
import { DiseaseService } from '../disease/services/disease.service';
import { PredictionHistory } from '../prediction/models/prediction.model';
import { DiseaseResponse } from '../disease/services/disease.service';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit, AfterViewChecked {
  isLoading = false;
  error: string | null = null;
  records: PredictionHistory[] = [];
  filteredRecords: PredictionHistory[] = [];

  // Date range filters
  dateFrom: string = '';
  dateTo: string = '';

  // Disease info cache (disease name -> disease info)
  diseaseInfoCache: Map<string, DiseaseResponse> = new Map();
  isLoadingDiseaseInfo: boolean = false;

  // Results Modal
  showResultsModal: boolean = false;
  selectedRecord: PredictionHistory | null = null;
  diseaseInfo: DiseaseResponse | null = null;
  allPredictions: Array<{disease: string, confidence: number}> = [];
  private shouldScrollToTop: boolean = false;

  @ViewChild('resultsContent', { static: false }) resultsContentRef!: ElementRef;

  constructor(
    private predictionService: PredictionService,
    private diseaseService: DiseaseService
  ) {}

  ngOnInit(): void {
    // Initialize date filters with default range (last 30 days)
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(today.getDate() - 30);
    this.dateTo = this.formatDateForInput(today);
    this.dateFrom = this.formatDateForInput(thirtyDaysAgo);
    
    // Load history after dates are set
    this.loadHistory();
  }

  ngAfterViewChecked(): void {
    if (this.shouldScrollToTop && this.resultsContentRef) {
      setTimeout(() => {
        if (this.resultsContentRef?.nativeElement) {
          this.resultsContentRef.nativeElement.scrollTop = 0;
          this.shouldScrollToTop = false;
        }
      }, 0);
    }
  }

  loadHistory(): void {
    this.isLoading = true;
    this.error = null;

    this.predictionService.getPredictionHistory(0, 100).pipe(
      finalize(() => (this.isLoading = false))
    ).subscribe({
      next: (response) => {
        this.records = response?.predictions || [];
        this.applyDateFilter();
        // Load disease info for all unique diseases
        this.loadDiseaseInfoForRecords();
      },
      error: () => {
        this.error = 'Unable to load your prediction history right now.';
      }
    });
  }

  /**
   * Load disease info for all unique diseases in records
   */
  loadDiseaseInfoForRecords(): void {
    // Get unique disease names
    const uniqueDiseases = Array.from(new Set(this.records.map(r => r.predicted_disease)));
    
    // Filter out diseases we already have cached
    const diseasesToFetch = uniqueDiseases.filter(disease => !this.diseaseInfoCache.has(disease));
    
    if (diseasesToFetch.length === 0) {
      return;
    }

    this.isLoadingDiseaseInfo = true;
    
    // Fetch disease info for all unique diseases using forkJoin
    const fetchObservables = diseasesToFetch.map(diseaseName => 
      this.diseaseService.searchDiseases(diseaseName)
    );

    forkJoin(fetchObservables).subscribe({
      next: (results) => {
        results.forEach((diseases, index) => {
          if (diseases && diseases.length > 0) {
            const diseaseName = diseasesToFetch[index];
            // Find exact match or use first result
            const exactMatch = diseases.find(d => 
              d.name.toLowerCase() === diseaseName.toLowerCase()
            );
            const diseaseInfo = exactMatch || diseases[0];
            this.diseaseInfoCache.set(diseaseName, diseaseInfo);
          }
        });
        this.isLoadingDiseaseInfo = false;
      },
      error: (error) => {
        console.error('Error loading disease info:', error);
        this.isLoadingDiseaseInfo = false;
      }
    });
  }

  /**
   * Format date for input field (YYYY-MM-DD)
   */
  formatDateForInput(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  /**
   * Format date for display (DD/MM/YYYY)
   */
  formatDate(timestamp: string): string {
    try {
      return new Intl.DateTimeFormat('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      }).format(new Date(timestamp));
    } catch {
      return timestamp;
    }
  }

  /**
   * Format date for display in input field (MMM DD, YYYY)
   */
  formatDateForDisplay(dateString: string): string {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: '2-digit',
        year: 'numeric'
      }).format(date);
    } catch {
      return dateString;
    }
  }

  /**
   * Apply date filter to records
   */
  applyDateFilter(): void {
    if (!this.dateFrom && !this.dateTo) {
      this.filteredRecords = this.records;
      return;
    }

    this.filteredRecords = this.records.filter(record => {
      const recordDate = new Date(record.timestamp);
      recordDate.setHours(0, 0, 0, 0);

      if (this.dateFrom) {
        const fromDate = new Date(this.dateFrom);
        fromDate.setHours(0, 0, 0, 0);
        if (recordDate < fromDate) return false;
      }

      if (this.dateTo) {
        const toDate = new Date(this.dateTo);
        toDate.setHours(23, 59, 59, 999);
        if (recordDate > toDate) return false;
      }

      return true;
    });
  }

  /**
   * Handle date filter change
   */
  onDateFilterChange(): void {
    this.applyDateFilter();
  }

  /**
   * Open results modal for a record
   */
  openRecordModal(record: PredictionHistory): void {
    this.selectedRecord = record;
    this.showResultsModal = true;
    this.isLoadingDiseaseInfo = true;
    this.diseaseInfo = null;
    this.allPredictions = [
      { disease: record.predicted_disease, confidence: record.confidence }
    ];

    // Get disease info from cache or fetch it
    const cachedInfo = this.diseaseInfoCache.get(record.predicted_disease);
    if (cachedInfo) {
      this.diseaseInfo = cachedInfo;
      this.isLoadingDiseaseInfo = false;
      this.shouldScrollToTop = true;
    } else {
      // Fetch disease info if not in cache
      this.diseaseService.searchDiseases(record.predicted_disease).subscribe({
        next: (diseases) => {
          if (diseases && diseases.length > 0) {
            // Find exact match or use first result
            const exactMatch = diseases.find(d => 
              d.name.toLowerCase() === record.predicted_disease.toLowerCase()
            );
            this.diseaseInfo = exactMatch || diseases[0];
            // Cache it for future use
            this.diseaseInfoCache.set(record.predicted_disease, this.diseaseInfo);
          }
          this.isLoadingDiseaseInfo = false;
          this.shouldScrollToTop = true;
        },
        error: (error) => {
          console.error('Error fetching disease info:', error);
          this.isLoadingDiseaseInfo = false;
          this.shouldScrollToTop = true;
        }
      });
    }
  }

  /**
   * Close results modal
   */
  closeResultsModal(): void {
    this.showResultsModal = false;
    this.selectedRecord = null;
    this.diseaseInfo = null;
    this.allPredictions = [];
  }

  /**
   * Get recommendations from disease info or generate default
   */
  getRecommendations(): string[] {
    if (this.diseaseInfo) {
      const recommendations: string[] = [];
      
      // Add precautions as recommendations
      if (this.diseaseInfo.precautions && Array.isArray(this.diseaseInfo.precautions) && this.diseaseInfo.precautions.length > 0) {
        recommendations.push(...this.diseaseInfo.precautions);
      }
      
      // Add recommendations from database (newline-separated string)
      if (this.diseaseInfo.recommendations) {
        const recs = this.diseaseInfo.recommendations
          .split('\n')
          .map((r: string) => r.trim())
          .filter((r: string) => r.length > 0);
        recommendations.push(...recs);
      }
      
      if (recommendations.length > 0) {
        const uniqueRecs = Array.from(new Set(recommendations));
        return uniqueRecs.length > 10 ? uniqueRecs.slice(0, 10) : uniqueRecs;
      }
    }
    
    // Default recommendations
    return this.getDefaultRecommendations();
  }

  /**
   * Get default recommendations
   */
  getDefaultRecommendations(): string[] {
    return [
      'Consult with a healthcare professional for proper diagnosis',
      'Follow any prescribed medications as directed',
      'Monitor your symptoms and seek medical attention if they worsen'
    ];
  }

  /**
   * Get disease description for a record
   */
  getDiseaseDescription(record: PredictionHistory): string {
    const diseaseInfo = this.diseaseInfoCache.get(record.predicted_disease);
    if (diseaseInfo?.description) {
      return diseaseInfo.description;
    }
    return 'Disease description not available';
  }

  /**
   * Get recommendations for a record from database
   */
  getRecommendationsForRecord(record: PredictionHistory): string[] {
    const diseaseInfo = this.diseaseInfoCache.get(record.predicted_disease);
    if (diseaseInfo) {
      const recommendations: string[] = [];
      
      // Add precautions as recommendations
      if (diseaseInfo.precautions && Array.isArray(diseaseInfo.precautions) && diseaseInfo.precautions.length > 0) {
        recommendations.push(...diseaseInfo.precautions);
      }
      
      // Add recommendations from database (newline-separated string)
      if (diseaseInfo.recommendations) {
        const recs = diseaseInfo.recommendations
          .split('\n')
          .map((r: string) => r.trim())
          .filter((r: string) => r.length > 0);
        recommendations.push(...recs);
      }
      
      if (recommendations.length > 0) {
        const uniqueRecs = Array.from(new Set(recommendations));
        return uniqueRecs;
      }
    }
    
    // Default recommendations if no disease info available
    return this.getDefaultRecommendations();
  }

}


