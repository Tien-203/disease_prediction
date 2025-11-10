import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface DoctorPatientRecord {
  dateRecorded: string;
  patientName: string;
  diseases: string[];
}

/**
 * Doctor patient records component
 */
@Component({
  selector: 'app-doctor-patients',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './doctor-patients.component.html',
  styleUrls: ['./doctor-patients.component.scss']
})
export class DoctorPatientsComponent {
  searchTerm = '';
  fromDate = 'Oct 12, 2021';
  toDate = 'Oct 17, 2021';

  dateModalOpen = false;
  activeDatePicker: 'from' | 'to' | null = null;

  readonly records: DoctorPatientRecord[] = [
    {
      dateRecorded: 'Oct 17, 2021',
      patientName: 'Alex Johnson',
      diseases: ['Influenza', 'Bronchitis', 'Hypertension']
    },
    {
      dateRecorded: 'Oct 15, 2021',
      patientName: 'Maria Chen',
      diseases: ['Migraine', 'Anxiety']
    },
    {
      dateRecorded: 'Oct 12, 2021',
      patientName: 'Samir Patel',
      diseases: ['Gastritis', 'Dehydration']
    }
  ];

  get filteredRecords(): DoctorPatientRecord[] {
    const term = this.searchTerm.trim().toLowerCase();
    if (!term) {
      return this.records;
    }
    return this.records.filter((record) =>
      record.patientName.toLowerCase().includes(term) ||
      record.diseases.some(disease => disease.toLowerCase().includes(term))
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

  exportPatients(): void {
    // Placeholder for export
  }
}

