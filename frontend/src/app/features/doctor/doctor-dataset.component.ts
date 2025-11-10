import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface DoctorDatasetRecord {
  dateModified: string;
  disease: string;
  questions: string[];
}

/**
 * Doctor dataset component
 */
@Component({
  selector: 'app-doctor-dataset',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './doctor-dataset.component.html',
  styleUrls: ['./doctor-dataset.component.scss']
})
export class DoctorDatasetComponent {
  searchTerm = '';
  fromDate = 'Oct 12, 2021';
  toDate = 'Oct 17, 2021';

  dateModalOpen = false;
  activeDatePicker: 'from' | 'to' | null = null;

  readonly records: DoctorDatasetRecord[] = [
    {
      dateModified: 'Oct 17, 2021',
      disease: 'Influenza',
      questions: ['Temperature check', 'Cough severity', 'Breathing difficulty']
    },
    {
      dateModified: 'Oct 15, 2021',
      disease: 'Migraine',
      questions: ['Pain location', 'Intensity scale', 'Light sensitivity']
    },
    {
      dateModified: 'Oct 13, 2021',
      disease: 'Gastritis',
      questions: ['Diet triggers', 'Stomach pain scale', 'Nausea frequency']
    }
  ];

  get filteredRecords(): DoctorDatasetRecord[] {
    const term = this.searchTerm.trim().toLowerCase();
    if (!term) {
      return this.records;
    }
    return this.records.filter((record) =>
      record.disease.toLowerCase().includes(term) ||
      record.questions.some(question => question.toLowerCase().includes(term))
    );
  }

  openDateModal(type: 'from' | 'to'): void {
    this.activeDatePicker = type;
    this.dateModalOpen = true;
  }

  closeDateModal(): void {
    this.dateModalOpen = false;
    this.activeDatePicker = null;
  }

  // Placeholder for export action
  exportDataset(): void {
    // Implementation can be added later
  }
}

