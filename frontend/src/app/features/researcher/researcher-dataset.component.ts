import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil } from 'rxjs';
import { ApiService } from '../../core/services/api.service';
import * as XLSX from 'xlsx';

interface ResearcherDatasetRecord {
  date_modified: string;
  disease: string;
  symptoms: string[];
}

/**
 * Researcher dataset component
 */
@Component({
  selector: 'app-researcher-dataset',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './researcher-dataset.component.html',
  styleUrls: ['./researcher-dataset.component.scss']
})
export class ResearcherDatasetComponent implements OnInit, OnDestroy {
  searchTerm = '';
  records: ResearcherDatasetRecord[] = [];
  isLoading = false;
  
  private destroy$ = new Subject<void>();

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadDataset();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  get filteredRecords(): ResearcherDatasetRecord[] {
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
    this.apiService.get<{ records: ResearcherDatasetRecord[]; total: number }>('/dataset/records')
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response: { records: ResearcherDatasetRecord[]; total: number }) => {
          this.records = response.records;
          this.isLoading = false;
        },
        error: (error: any) => {
          console.error('Error loading dataset:', error);
          this.isLoading = false;
        }
      });
  }

  exportDataset(): void {
    try {
      // Prepare data for export
      const exportData = this.filteredRecords.map(record => ({
        'Date Modified': record.date_modified,
        'Disease': record.disease,
        'Symptoms': record.symptoms.join(', ')
      }));

      // Create workbook and worksheet
      const ws = XLSX.utils.json_to_sheet(exportData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Dataset');

      // Generate filename with current date
      const date = new Date().toISOString().split('T')[0];
      const filename = `dataset_export_${date}.xlsx`;

      // Write file
      XLSX.writeFile(wb, filename);
    } catch (error) {
      console.error('Error exporting dataset:', error);
      alert('Failed to export dataset. Please try again.');
    }
  }
}

