import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PredictionService } from '../prediction/services/prediction.service';
import { PatientPrediction, PredictionUpdateRequest } from '../prediction/models/prediction.model';
import * as XLSX from 'xlsx';

/**
 * Researcher patient records component
 */
@Component({
  selector: 'app-researcher-patients',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './researcher-patients.component.html',
  styleUrls: ['./researcher-patients.component.scss']
})
export class ResearcherPatientsComponent implements OnInit {
  searchTerm = '';
  fromDate: Date | null = null;
  toDate: Date | null = null;
  fromDateDisplay = 'Select date';
  toDateDisplay = 'Select date';

  dateModalOpen = false;
  activeDatePicker: 'from' | 'to' | null = null;
  correctModalOpen = false;
  selectedPrediction: PatientPrediction | null = null;
  correctedDiseaseInput = '';
  loading = false;
  correcting = false;

  records: PatientPrediction[] = [];

  // Calendar state
  currentMonth = new Date().getMonth();
  currentYear = new Date().getFullYear();

  constructor(private predictionService: PredictionService) {}

  ngOnInit(): void {
    this.loadPredictions();
  }

  /**
   * Load predictions from database
   */
  loadPredictions(): void {
    this.loading = true;
    this.predictionService.getAllPatientPredictions(0, 100).subscribe({
      next: (predictions: PatientPrediction[]) => {
        this.records = predictions;
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Error loading predictions:', err);
        this.loading = false;
      }
    });
  }

  /**
   * Format date for display
   */
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  }

  /**
   * Get filtered records based on search term and date range
   */
  get filteredRecords(): PatientPrediction[] {
    let filtered = this.records;

    // Filter by date range
    if (this.fromDate || this.toDate) {
      filtered = filtered.filter((record) => {
        const recordDate = new Date(record.timestamp);
        recordDate.setHours(0, 0, 0, 0);

        if (this.fromDate && this.toDate) {
          const from = new Date(this.fromDate);
          from.setHours(0, 0, 0, 0);
          const to = new Date(this.toDate);
          to.setHours(23, 59, 59, 999);
          return recordDate >= from && recordDate <= to;
        } else if (this.fromDate) {
          const from = new Date(this.fromDate);
          from.setHours(0, 0, 0, 0);
          return recordDate >= from;
        } else if (this.toDate) {
          const to = new Date(this.toDate);
          to.setHours(23, 59, 59, 999);
          return recordDate <= to;
        }
        return true;
      });
    }

    // Filter by search term
    const term = this.searchTerm.trim().toLowerCase();
    if (term) {
      filtered = filtered.filter((record) =>
        (record.user_name || '').toLowerCase().includes(term) ||
        (record.predicted_disease || '').toLowerCase().includes(term) ||
        (record.corrected_disease || '').toLowerCase().includes(term)
      );
    }

    return filtered;
  }

  /**
   * Open date modal
   */
  openDateModal(type: 'from' | 'to'): void {
    this.activeDatePicker = type;
    this.dateModalOpen = true;
    // Set calendar to show the selected date or current date
    if (type === 'from' && this.fromDate) {
      this.currentMonth = this.fromDate.getMonth();
      this.currentYear = this.fromDate.getFullYear();
    } else if (type === 'to' && this.toDate) {
      this.currentMonth = this.toDate.getMonth();
      this.currentYear = this.toDate.getFullYear();
    }
  }

  /**
   * Close date modal
   */
  closeDateModal(): void {
    this.dateModalOpen = false;
    this.activeDatePicker = null;
  }

  /**
   * Select a date from the calendar
   */
  selectDate(day: number): void {
    if (!this.activeDatePicker) return;

    const selectedDate = new Date(this.currentYear, this.currentMonth, day);
    
    if (this.activeDatePicker === 'from') {
      this.fromDate = selectedDate;
      this.fromDateDisplay = this.formatDateDisplay(selectedDate);
      // If toDate is set and fromDate is after toDate, clear toDate
      if (this.toDate && selectedDate > this.toDate) {
        this.toDate = null;
        this.toDateDisplay = 'Select date';
      }
    } else {
      this.toDate = selectedDate;
      this.toDateDisplay = this.formatDateDisplay(selectedDate);
      // If fromDate is set and toDate is before fromDate, clear fromDate
      if (this.fromDate && selectedDate < this.fromDate) {
        this.fromDate = null;
        this.fromDateDisplay = 'Select date';
      }
    }
    
    // Don't close modal - allow user to navigate and select dates far apart
    // User can close manually with X button
  }

  /**
   * Format date for display in chips
   */
  formatDateDisplay(date: Date): string {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  /**
   * Navigate to previous month
   */
  previousMonth(): void {
    if (this.currentMonth === 0) {
      this.currentMonth = 11;
      this.currentYear--;
    } else {
      this.currentMonth--;
    }
  }

  /**
   * Navigate to next month
   */
  nextMonth(): void {
    if (this.currentMonth === 11) {
      this.currentMonth = 0;
      this.currentYear++;
    } else {
      this.currentMonth++;
    }
  }

  /**
   * Get calendar days for current month
   */
  getCalendarDays(): { day: number; isCurrentMonth: boolean }[] {
    const days: { day: number; isCurrentMonth: boolean }[] = [];
    const firstDay = new Date(this.currentYear, this.currentMonth, 1).getDay();
    const daysInMonth = new Date(this.currentYear, this.currentMonth + 1, 0).getDate();
    const daysInPrevMonth = new Date(this.currentYear, this.currentMonth, 0).getDate();

    // Adjust first day (0 = Sunday, we want Monday = 0)
    const adjustedFirstDay = firstDay === 0 ? 6 : firstDay - 1;

    // Add previous month's trailing days
    for (let i = adjustedFirstDay - 1; i >= 0; i--) {
      days.push({ day: daysInPrevMonth - i, isCurrentMonth: false });
    }

    // Add current month's days
    for (let i = 1; i <= daysInMonth; i++) {
      days.push({ day: i, isCurrentMonth: true });
    }

    // Fill remaining cells to complete the grid (42 cells total for 6 weeks)
    const remainingCells = 42 - days.length;
    for (let i = 1; i <= remainingCells; i++) {
      days.push({ day: i, isCurrentMonth: false });
    }

    return days;
  }

  /**
   * Get current month name
   */
  getCurrentMonthName(): string {
    return new Date(this.currentYear, this.currentMonth).toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  }

  /**
   * Check if a date is selected
   */
  isDateSelected(day: number): boolean {
    if (!this.activeDatePicker) return false;
    const checkDate = new Date(this.currentYear, this.currentMonth, day);
    
    if (this.activeDatePicker === 'from' && this.fromDate) {
      return checkDate.getTime() === this.fromDate.getTime();
    } else if (this.activeDatePicker === 'to' && this.toDate) {
      return checkDate.getTime() === this.toDate.getTime();
    }
    return false;
  }

  /**
   * Clear date filters
   */
  clearDateFilters(): void {
    this.fromDate = null;
    this.toDate = null;
    this.fromDateDisplay = 'Select date';
    this.toDateDisplay = 'Select date';
  }

  /**
   * Open correct prediction modal
   */
  openCorrectModal(prediction: PatientPrediction): void {
    this.selectedPrediction = prediction;
    this.correctedDiseaseInput = prediction.corrected_disease || '';
    this.correctModalOpen = true;
  }

  /**
   * Close correct prediction modal
   */
  closeCorrectModal(): void {
    this.correctModalOpen = false;
    this.selectedPrediction = null;
    this.correctedDiseaseInput = '';
  }

  /**
   * Save corrected prediction
   */
  saveCorrectedPrediction(): void {
    if (!this.selectedPrediction || !this.correctedDiseaseInput.trim()) {
      return;
    }

    this.correcting = true;
    const request: PredictionUpdateRequest = {
      corrected_disease: this.correctedDiseaseInput.trim()
    };

    this.predictionService.correctPrediction(this.selectedPrediction.id, request).subscribe({
      next: () => {
        // Reload predictions to get updated recommendation
        this.loadPredictions();
        this.closeCorrectModal();
        this.correcting = false;
      },
      error: (err: any) => {
        console.error('Error correcting prediction:', err);
        this.correcting = false;
        alert('Failed to correct prediction. Please try again.');
      }
    });
  }

  /**
   * Export patients to Excel
   */
  exportPatients(): void {
    try {
      // Prepare data for export using filtered records
      const exportData = this.filteredRecords.map(record => ({
        'Date': this.formatDate(record.timestamp),
        'Patient Name': record.user_name || 'N/A',
        'Age': record.user_age || 'N/A',
        'Gender': record.user_gender || 'N/A',
        'Predicted Disease': record.predicted_disease,
        'Confidence': (record.confidence * 100).toFixed(2) + '%',
        'Corrected Disease': record.corrected_disease || '',
        'Recommendation': record.recommendation || '',
        'Symptoms': record.symptoms.join(', ')
      }));

      // Create workbook and worksheet
      const ws = XLSX.utils.json_to_sheet(exportData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Patient Log');

      // Set column widths
      const colWidths = [
        { wch: 12 }, // Date
        { wch: 20 }, // Patient Name
        { wch: 5 },  // Age
        { wch: 10 }, // Gender
        { wch: 25 }, // Predicted Disease
        { wch: 12 }, // Confidence
        { wch: 25 }, // Corrected Disease
        { wch: 50 }, // Recommendation
        { wch: 40 }  // Symptoms
      ];
      ws['!cols'] = colWidths;

      // Generate filename with current date
      const date = new Date().toISOString().split('T')[0];
      const filename = `patient_log_export_${date}.xlsx`;

      // Write file
      XLSX.writeFile(wb, filename);
    } catch (error) {
      console.error('Error exporting patient log:', error);
      alert('Failed to export patient log. Please try again.');
    }
  }
}

