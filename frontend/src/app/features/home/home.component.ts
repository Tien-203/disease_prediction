import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { PredictionService } from '../prediction/services/prediction.service';
import { SymptomGroup, SymptomOption } from '../prediction/models/symptom.model';
import { PredictionRequest, PredictionResponse } from '../prediction/models/prediction.model';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, AfterViewChecked {
  userName: string = 'Patient';

  // Quick Check Modal
  showQuickCheckModal: boolean = false;
  symptomGroups: SymptomGroup[] = [];
  currentGroupIndex: number = 0;
  selectedSymptoms: Set<number> = new Set();
  isLoadingGroups: boolean = false;
  isProcessing: boolean = false;

  // Results Modal
  showResultsModal: boolean = false;
  predictionResult: any = null;
  allPredictions: Array<{disease: string, confidence: number}> = [];
  private shouldScrollToTop: boolean = false;

  @ViewChild('resultsContent', { static: false }) resultsContentRef!: ElementRef;

  // Confirm Submit Modal
  showConfirmSubmitModal: boolean = false;
  pendingSubmitAction: 'submit' | 'skip' | null = null;

  // Describe Symptoms Modal
  showDescribeModal: boolean = false;
  symptomDescription: string = '';

  constructor(
    private authService: AuthService,
    private predictionService: PredictionService,
    private router: Router
  ) {}

  ngOnInit(): void {
    console.log('HomeComponent initialized');
    const currentUser = this.authService.getCurrentUser();
    console.log('Current user in HomeComponent:', currentUser);
    if (currentUser?.name) {
      this.userName = currentUser.name;
    } else if (currentUser?.email) {
      this.userName = currentUser.email.split('@')[0];
    }
  }

  /**
   * Scroll to top of results content after view update
   */
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

  /**
   * Open Quick Check modal and load symptom groups
   */
  openQuickCheckModal(): void {
    this.showQuickCheckModal = true;
    this.currentGroupIndex = 0;
    this.selectedSymptoms.clear();
    this.loadSymptomGroups();
  }

  /**
   * Close Quick Check modal
   */
  closeQuickCheckModal(): void {
    this.showQuickCheckModal = false;
    this.currentGroupIndex = 0;
    this.selectedSymptoms.clear();
    this.symptomGroups = [];
  }

  /**
   * Load symptom groups from API
   */
  loadSymptomGroups(): void {
    this.isLoadingGroups = true;
    this.predictionService.getGroupedSymptoms().subscribe({
      next: (response) => {
        this.symptomGroups = response.groups;
        this.isLoadingGroups = false;
      },
      error: (error) => {
        console.error('Error loading symptom groups:', error);
        this.isLoadingGroups = false;
        alert('Failed to load symptom groups. Please try again.');
      }
    });
  }

  /**
   * Get current symptom group
   */
  getCurrentGroup(): SymptomGroup | null {
    if (this.currentGroupIndex >= 0 && this.currentGroupIndex < this.symptomGroups.length) {
      return this.symptomGroups[this.currentGroupIndex];
    }
    return null;
  }

  /**
   * Check if symptom is selected
   */
  isSymptomSelected(symptomId: number): boolean {
    return this.selectedSymptoms.has(symptomId);
  }

  /**
   * Toggle symptom selection
   */
  toggleSymptom(symptomId: number): void {
    const currentGroup = this.getCurrentGroup();
    if (!currentGroup) return;

    console.log(`Toggling symptom ${symptomId} in group ${this.currentGroupIndex}`);
    console.log(`Current selected symptoms before toggle:`, Array.from(this.selectedSymptoms));

    if (currentGroup.allow_multiple) {
      // Multiple selection allowed
      if (this.selectedSymptoms.has(symptomId)) {
        this.selectedSymptoms.delete(symptomId);
        console.log(`  Removed symptom ${symptomId}`);
      } else {
        this.selectedSymptoms.add(symptomId);
        console.log(`  Added symptom ${symptomId}`);
      }
    } else {
      // Single selection only - clear only symptoms from current group
      // First, remove all symptoms from the current group
      const removedIds: number[] = [];
      currentGroup.options.forEach(option => {
        if (this.selectedSymptoms.has(option.id)) {
          this.selectedSymptoms.delete(option.id);
          removedIds.push(option.id);
        }
      });
      if (removedIds.length > 0) {
        console.log(`  Cleared symptoms from current group:`, removedIds);
      }
      // Then add the newly selected symptom
      this.selectedSymptoms.add(symptomId);
      console.log(`  Added symptom ${symptomId}`);
    }
    
    console.log(`Current selected symptoms after toggle:`, Array.from(this.selectedSymptoms));
  }

  /**
   * Go to next question
   */
  nextQuestion(): void {
    console.log(`Moving to next question. Current index: ${this.currentGroupIndex}, Total groups: ${this.symptomGroups.length}`);
    console.log(`Selected symptoms before moving:`, Array.from(this.selectedSymptoms));
    
    if (this.currentGroupIndex < this.symptomGroups.length - 1) {
      this.currentGroupIndex++;
      console.log(`Moved to question ${this.currentGroupIndex + 1}. Selected symptoms:`, Array.from(this.selectedSymptoms));
    } else {
      // All questions answered, check if we have symptoms before submitting
      console.log(`All questions answered. Total selected symptoms: ${this.selectedSymptoms.size}`);
      if (this.selectedSymptoms.size === 0) {
        alert('Please select at least one symptom before submitting.');
        return;
      }
      // Show confirm modal before submitting
      this.pendingSubmitAction = 'submit';
      this.showConfirmSubmitModal = true;
    }
  }

  /**
   * Go to previous question
   */
  previousQuestion(): void {
    if (this.currentGroupIndex > 0) {
      this.currentGroupIndex--;
    }
  }

  /**
   * Skip current question
   */
  skipQuestion(): void {
    console.log(`Skipping question ${this.currentGroupIndex + 1}. Selected symptoms before skip:`, Array.from(this.selectedSymptoms));
    
    // If this is the last question, show confirm modal
    if (this.currentGroupIndex === this.symptomGroups.length - 1) {
      this.pendingSubmitAction = 'skip';
      this.showConfirmSubmitModal = true;
      return;
    }

    // DO NOT clear selections for current group - keep them when skipping
    // Just move to next question
    this.nextQuestion();
    console.log(`Skipped question. Selected symptoms after skip:`, Array.from(this.selectedSymptoms));
  }

  /**
   * Check if can proceed to next question
   */
  canProceed(): boolean {
    const currentGroup = this.getCurrentGroup();
    if (!currentGroup) return false;
    
    // Check if at least one symptom is selected from current group
    const hasSelectionFromCurrentGroup = currentGroup.options.some(
      option => this.selectedSymptoms.has(option.id)
    );
    
    return hasSelectionFromCurrentGroup;
  }

  /**
   * Get progress percentage
   */
  getProgress(): number {
    if (this.symptomGroups.length === 0) return 0;
    return ((this.currentGroupIndex + 1) / this.symptomGroups.length) * 100;
  }

  /**
   * Get count of selected symptoms
   */
  getSelectedSymptomsCount(): number {
    return this.selectedSymptoms.size;
  }

  /**
   * Confirm and proceed with submit
   */
  confirmSubmit(): void {
    this.showConfirmSubmitModal = false;
    
    // DO NOT clear selections when skipping - keep all selected symptoms
    // The skip action just means "move to next question without requiring selection"
    
    // Check if we have symptoms
    const symptomNames: string[] = [];
    this.symptomGroups.forEach(group => {
      group.options.forEach(option => {
        if (this.selectedSymptoms.has(option.id)) {
          symptomNames.push(option.name);
        }
      });
    });

    if (symptomNames.length === 0) {
      alert('Please select at least one symptom before submitting.');
      this.pendingSubmitAction = null;
      return;
    }

    // Proceed with submission
    this.pendingSubmitAction = null;
    this.submitQuickCheck();
  }

  /**
   * Cancel confirm submit
   */
  cancelConfirmSubmit(): void {
    this.showConfirmSubmitModal = false;
    this.pendingSubmitAction = null;
  }

  /**
   * Submit Quick Check prediction
   */
  submitQuickCheck(): void {
    // Get symptom names from selected IDs first
    const symptomNames: string[] = [];
    
    // Debug: Log all groups and their options
    console.log('All symptom groups:', this.symptomGroups);
    console.log('Selected symptom IDs:', Array.from(this.selectedSymptoms));
    
    // Collect symptoms from all groups
    this.symptomGroups.forEach((group, groupIndex) => {
      console.log(`Group ${groupIndex} (${group.question}):`, group.options);
      group.options.forEach(option => {
        if (this.selectedSymptoms.has(option.id)) {
          console.log(`  Found selected symptom: ${option.name} (ID: ${option.id})`);
          symptomNames.push(option.name);
        }
      });
    });

    // Remove duplicates and get unique symptom names
    const uniqueSymptomNames = Array.from(new Set(symptomNames));

    // Debug log to verify all symptoms are collected
    console.log('Total selected symptom IDs:', this.selectedSymptoms.size);
    console.log('Collected symptom names (with duplicates):', symptomNames);
    console.log('Unique symptom names:', uniqueSymptomNames);
    console.log('Unique symptom count:', uniqueSymptomNames.length);

    // Validate that we have at least one symptom
    if (uniqueSymptomNames.length === 0) {
      alert('Please select at least one symptom before submitting.');
      return;
    }

    // Close quick check modal first
    this.closeQuickCheckModal();
    
    // Show results modal with loading state
    this.showResultsModal = true;
    this.isProcessing = true;

    const request: PredictionRequest = {
      symptoms: uniqueSymptomNames,  // Use unique symptoms only
      session_id: `quick-check-${Date.now()}`
    };

    this.predictionService.predictDisease(request).subscribe({
      next: (response: PredictionResponse) => {
        this.predictionResult = response;
        
        // Prepare all predictions (main + alternatives)
        this.allPredictions = [
          { disease: response.predicted_disease, confidence: response.confidence },
          ...response.alternatives.map(alt => ({
            disease: alt.disease,
            confidence: alt.confidence
          }))
        ].sort((a, b) => b.confidence - a.confidence); // Sort by confidence descending
        
        // Hide loading and show results
        this.isProcessing = false;
        // Trigger scroll to top after view update
        this.shouldScrollToTop = true;
      },
      error: (error) => {
        console.error('Error predicting disease:', error);
        this.isProcessing = false;
        this.closeResultsModal();
        alert('Failed to get prediction. Please try again.');
      }
    });
  }

  /**
   * Open Describe Symptoms modal
   */
  openDescribeModal(): void {
    this.showDescribeModal = true;
    this.symptomDescription = '';
  }

  /**
   * Close Describe Symptoms modal
   */
  closeDescribeModal(): void {
    this.showDescribeModal = false;
    this.symptomDescription = '';
  }

  /**
   * Submit description and continue
   */
  submitDescription(): void {
    if (!this.symptomDescription.trim()) {
      alert('Please describe your symptoms.');
      return;
    }

    // For now, navigate to prediction page with the description
    // In a real implementation, you might want to process the text
    // and extract symptoms using NLP or show a symptom selection interface
    this.closeDescribeModal();
    this.router.navigate(['/prediction'], { 
      state: { description: this.symptomDescription } 
    });
  }

  /**
   * Close Results Modal
   */
  closeResultsModal(): void {
    this.showResultsModal = false;
    this.predictionResult = null;
    this.allPredictions = [];
  }

  /**
   * Get recommendations from prediction result (from database)
   */
  getRecommendations(): string[] {
    if (!this.predictionResult?.disease_info) {
      return this.getDefaultRecommendations();
    }
    
    const info = this.predictionResult.disease_info;
    const recommendations: string[] = [];
    
    // Add precautions as recommendations (precautions is an array)
    if (info.precautions && Array.isArray(info.precautions) && info.precautions.length > 0) {
      recommendations.push(...info.precautions);
    }
    
    // Add general recommendations from database (recommendations is a string, newline-separated)
    if (info.recommendations) {
      if (typeof info.recommendations === 'string') {
        // Split by newlines (recommendations are stored as newline-separated in DB)
        const recs = info.recommendations
          .split('\n')
          .map((r: string) => r.trim())
          .filter((r: string) => r.length > 0);
        recommendations.push(...recs);
      } else if (Array.isArray(info.recommendations)) {
        recommendations.push(...info.recommendations);
      }
    }
    
    // If no recommendations from database, provide default ones
    if (recommendations.length === 0) {
      return this.getDefaultRecommendations();
    }
    
    // Remove duplicates and return all (or limit if too many)
    const uniqueRecs = Array.from(new Set(recommendations));
    return uniqueRecs.length > 10 ? uniqueRecs.slice(0, 10) : uniqueRecs;
  }

  /**
   * Get default recommendations when no specific recommendations are available
   */
  getDefaultRecommendations(): string[] {
    return [
      'Consult with a healthcare professional for proper diagnosis',
      'Follow any prescribed medications as directed',
      'Monitor your symptoms and seek medical attention if they worsen'
    ];
  }

  /**
   * Navigate to record new disease page
   */
  navigateToRecordDisease(): void {
    // Navigate to a page where users can record new diseases
    // For now, we'll just show an alert or navigate to a placeholder
    alert('Record new disease feature coming soon!');
    // this.router.navigate(['/diseases/new']);
  }

  /**
   * Navigate to record new disease from results modal
   */
  navigateToRecordDiseaseFromResults(): void {
    this.closeResultsModal();
    this.navigateToRecordDisease();
  }
}
