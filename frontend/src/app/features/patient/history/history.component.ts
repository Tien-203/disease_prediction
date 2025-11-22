import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PredictionService, PredictionHistory } from '../../services/prediction.service';
import { ConfidencePipe } from '../../../shared/pipes/confidence.pipe';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { ErrorHandlerService } from '../../../core/services/error-handler.service';
import { LoggerService } from '../../../core/services/logger.service';

/**
 * Patient prediction history component
 */
@Component({
  selector: 'app-history',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatPaginatorModule,
    MatFormFieldModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    ConfidencePipe
  ],
  templateUrl: './history.component.html',
  styleUrl: './history.component.scss'
})
export class HistoryComponent implements OnInit {
  predictions: PredictionHistory[] = [];
  displayedColumns: string[] = ['timestamp', 'symptoms', 'predicted_disease', 'confidence', 'actions'];
  total = 0;
  pageSize = 10;
  pageIndex = 0;
  isLoading = false;
  errorMessage = '';

  constructor(
    private predictionService: PredictionService,
    private errorHandler: ErrorHandlerService,
    private logger: LoggerService
  ) {}

  ngOnInit(): void {
    this.loadHistory();
  }

  /**
   * Load prediction history
   */
  loadHistory(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.predictionService.getHistory(
      this.pageIndex * this.pageSize,
      this.pageSize
    ).subscribe({
      next: (response) => {
        this.predictions = response.predictions;
        this.total = response.total;
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = this.errorHandler.handleError(error);
        this.isLoading = false;
      }
    });
  }

  /**
   * Handle page change
   */
  onPageChange(event: PageEvent): void {
    this.pageIndex = event.pageIndex;
    this.pageSize = event.pageSize;
    this.loadHistory();
  }

  /**
   * Format date for display
   */
  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleString();
  }
}
