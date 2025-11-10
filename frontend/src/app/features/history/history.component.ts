import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PredictionService } from '../prediction/services/prediction.service';
import { PredictionHistory } from '../prediction/models/prediction.model';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {
  isLoading = false;
  error: string | null = null;
  records: PredictionHistory[] = [];

  constructor(private predictionService: PredictionService) {}

  ngOnInit(): void {
    this.loadHistory();
  }

  loadHistory(): void {
    this.isLoading = true;
    this.error = null;

    this.predictionService.getPredictionHistory(0, 20).pipe(
      finalize(() => (this.isLoading = false))
    ).subscribe({
      next: (response) => {
        this.records = response?.predictions || [];
      },
      error: () => {
        this.error = 'Unable to load your prediction history right now.';
      }
    });
  }

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

  generateRecommendations(record: PredictionHistory): string[] {
    const highlightedSymptoms = record.symptoms.slice(0, 3).join(', ') || 'your noted symptoms';
    return [
      `Monitor ${highlightedSymptoms}.`,
      `Schedule a follow-up on ${record.predicted_disease}.`,
      'Stay hydrated, well-rested, and seek medical advice if symptoms persist.'
    ];
  }
}


