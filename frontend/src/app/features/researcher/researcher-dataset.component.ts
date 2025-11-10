import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface ResearcherDatasetRecord {
  dateModified: string;
  disease: string;
  questions: string[];
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
export class ResearcherDatasetComponent {
  searchTerm = '';
  fromDate = 'Oct 12, 2021';
  toDate = 'Oct 17, 2021';

  dateModalOpen = false;
  activeDatePicker: 'from' | 'to' | null = null;

  readonly records: ResearcherDatasetRecord[] = [
    {
      dateModified: 'Oct 17, 2021',
      disease: 'Influenza',
      questions: ['Temperature check', 'Travel history', 'Vaccination status']
    },
    {
      dateModified: 'Oct 15, 2021',
      disease: 'Diabetes Type II',
      questions: ['Blood sugar average', 'Medication adherence', 'Lifestyle notes']
    },
    {
      dateModified: 'Oct 12, 2021',
      disease: 'Hypertension',
      questions: ['BP readings', 'Diet tracking', 'Stress level']
    }
  ];

  get filteredRecords(): ResearcherDatasetRecord[] {
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

  exportDataset(): void {
    // Placeholder for export action
  }
}

