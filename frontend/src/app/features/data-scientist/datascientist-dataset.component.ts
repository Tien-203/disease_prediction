import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface DatasetRecord {
  dateModified: string;
  disease: string;
  questions: string[];
}

/**
 * Data Scientist dataset component
 */
@Component({
  selector: 'app-datascientist-dataset',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './datascientist-dataset.component.html',
  styleUrls: ['./datascientist-dataset.component.scss']
})
export class DataScientistDatasetComponent {
  records: DatasetRecord[] = [
    {
      dateModified: '02/10/2025',
      disease: 'Seasonal Influenza',
      questions: ['Fever duration', 'Cough intensity', 'Travel history']
    },
    {
      dateModified: '25/09/2025',
      disease: 'Migraine',
      questions: ['Pain location', 'Light sensitivity', 'Medication response']
    },
    {
      dateModified: '18/09/2025',
      disease: 'Gastroenteritis',
      questions: ['Symptoms onset', 'Hydration level', 'Diet triggers']
    }
  ];
}

