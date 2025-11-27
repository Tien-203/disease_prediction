import { Component, OnDestroy, OnInit, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth.service';
import { PredictionService } from '../prediction/services/prediction.service';
import { ApiService } from '../../core/services/api.service';
import { SymptomGroup, SymptomOption } from '../prediction/models/symptom.model';

type AddWizardStep = 'name' | 'symptoms' | 'saving' | 'success';
type ModifyWizardStep = 'search' | 'symptoms' | 'saving' | 'success';

// Extended symptom group with UI state
interface ExtendedSymptomGroup extends SymptomGroup {
  expanded: boolean;
  selectedSymptoms: number[]; // Array of selected symptom IDs
}

/**
 * Data Scientist dashboard component
 * Provides quick actions to maintain disease datasets
 */
@Component({
  selector: 'app-datascientist-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './datascientist-dashboard.component.html',
  styleUrls: ['./datascientist-dashboard.component.scss']
})
export class DataScientistDashboardComponent implements OnInit, OnDestroy {
  displayName = 'Data Scientist';

  addWizardOpen = false;
  addStep: AddWizardStep = 'name';
  readonly addStepOrder: AddWizardStep[] = ['name', 'symptoms', 'saving', 'success'];
  addDiseaseName = '';
  addWizardError: string | null = null;
  addSymptomGroups: ExtendedSymptomGroup[] = [];
  addHighlightedGroup: number | null = null;
  isLoadingGroups = false;

  modifyWizardOpen = false;
  modifyStep: ModifyWizardStep = 'search';
  readonly modifyStepOrder: ModifyWizardStep[] = ['search', 'symptoms', 'saving', 'success'];
  modifyWizardError: string | null = null;
  modifySearch = '';
  selectedDisease = '';
  modifySymptomGroups: ExtendedSymptomGroup[] = [];
  modifyHighlightedGroup: number | null = null;
  showDeleteConfirmation = false;
  isDeleting = false;

  private timeoutHandle?: number;

  constructor(
    private authService: AuthService,
    private predictionService: PredictionService,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser?.name) {
      this.displayName = currentUser.name;
    } else if (currentUser?.email) {
      this.displayName = currentUser.email;
    }
  }

  /**
   * Load symptom groups from API
   */
  loadSymptomGroups(): void {
    this.isLoadingGroups = true;
    this.predictionService.getGroupedSymptoms().subscribe({
      next: (response) => {
        // Convert API response to ExtendedSymptomGroup format
        this.addSymptomGroups = response.groups.map(group => ({
          ...group,
          expanded: false,
          selectedSymptoms: []
        }));
        this.modifySymptomGroups = response.groups.map(group => ({
          ...group,
          expanded: false,
          selectedSymptoms: []
        }));
        this.isLoadingGroups = false;
      },
      error: (error) => {
        console.error('Error loading symptom groups:', error);
        this.isLoadingGroups = false;
        this.addWizardError = 'Failed to load symptom groups. Please try again.';
      }
    });
  }

  ngOnDestroy(): void {
    this.clearPendingTimeout();
  }

  // --- Add disease wizard --------------------------------------------------

  openAddWizard(): void {
    this.resetAddWizard();
    this.addWizardOpen = true;
    // Load symptom groups when opening the wizard
    if (this.addSymptomGroups.length === 0) {
      this.loadSymptomGroups();
    }
  }

  closeAddWizard(): void {
    this.clearPendingTimeout();
    this.addWizardOpen = false;
  }

  continueAddWizard(): void {
    switch (this.addStep) {
      case 'name':
        if (!this.addDiseaseName.trim()) {
          this.addWizardError = 'Please enter the disease name before continuing.';
          return;
        }
        this.addWizardError = null;
        this.addStep = 'symptoms';
        break;
      case 'symptoms':
        // Check if at least one symptom is selected from any group
        const hasSelectedSymptoms = this.addSymptomGroups.some(group => group.selectedSymptoms.length > 0);
        if (!hasSelectedSymptoms) {
          this.addWizardError = 'Please select at least one symptom for this disease.';
          return;
        }
        this.addWizardError = null;
        this.addStep = 'saving';
        this.saveDiseaseWithSymptoms();
        break;
      case 'success':
        this.closeAddWizard();
        break;
      default:
        break;
    }
  }

  toggleSymptomGroup(index: number, event?: Event): void {
    // Prevent event bubbling to avoid closing immediately
    if (event) {
      event.stopPropagation();
    }
    
    // Close other groups if opening this one
    const wasExpanded = this.addSymptomGroups[index].expanded;
    this.addSymptomGroups.forEach((group, idx) => {
      if (idx !== index) {
        group.expanded = false;
      }
    });
    
    // Toggle expand/collapse
    this.addSymptomGroups[index].expanded = !wasExpanded;
    this.addHighlightedGroup = index;
  }

  selectSymptomGroup(index: number): void {
    this.addHighlightedGroup = index;
  }

  toggleSymptomInGroup(groupIndex: number, symptomId: number): void {
    const group = this.addSymptomGroups[groupIndex];
    const index = group.selectedSymptoms.indexOf(symptomId);
    
    if (index > -1) {
      // Remove symptom
      group.selectedSymptoms = group.selectedSymptoms.filter(id => id !== symptomId);
    } else {
      // Add symptom
      if (group.allow_multiple) {
        group.selectedSymptoms.push(symptomId);
      } else {
        // Single selection - replace all
        group.selectedSymptoms = [symptomId];
      }
    }
  }

  isSymptomSelected(groupIndex: number, symptomId: number): boolean {
    return this.addSymptomGroups[groupIndex].selectedSymptoms.includes(symptomId);
  }

  /**
   * Format group ID to display name
   */
  formatGroupName(groupId: string): string {
    return groupId
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (l) => l.toUpperCase());
  }

  private resetAddWizard(): void {
    this.clearPendingTimeout();
    this.addStep = 'name';
    this.addDiseaseName = '';
    this.addWizardError = null;
    this.addSymptomGroups = this.addSymptomGroups.map(group => ({
      ...group,
      expanded: false,
      selectedSymptoms: []
    }));
    this.addHighlightedGroup = null;
  }

  // --- Modify disease wizard -----------------------------------------------

  openModifyWizard(): void {
    this.resetModifyWizard();
    this.modifyWizardOpen = true;
    // Load symptom groups when opening the wizard
    if (this.modifySymptomGroups.length === 0) {
      this.loadSymptomGroups();
    }
  }

  closeModifyWizard(): void {
    this.clearPendingTimeout();
    this.modifyWizardOpen = false;
  }

  continueModifyWizard(): void {
    switch (this.modifyStep) {
      case 'search':
        if (!this.modifySearch.trim()) {
          this.modifyWizardError = 'Please enter a disease name to search.';
          return;
        }
        this.modifyWizardError = null;
        this.searchAndLoadDisease(this.modifySearch.trim());
        break;
      case 'symptoms':
        // Check if at least one symptom is selected from any group
        const hasSelectedSymptoms = this.modifySymptomGroups.some(group => group.selectedSymptoms.length > 0);
        if (!hasSelectedSymptoms) {
          this.modifyWizardError = 'Please select at least one symptom for this disease.';
          return;
        }
        this.modifyWizardError = null;
        this.modifyStep = 'saving';
        this.updateDiseaseSymptoms();
        break;
      case 'success':
        this.closeModifyWizard();
        break;
      default:
        break;
    }
  }

  toggleModifySymptomGroup(index: number, event?: Event): void {
    // Prevent event bubbling to avoid closing immediately
    if (event) {
      event.stopPropagation();
    }
    
    // Close other groups if opening this one
    const wasExpanded = this.modifySymptomGroups[index].expanded;
    this.modifySymptomGroups.forEach((group, idx) => {
      if (idx !== index) {
        group.expanded = false;
      }
    });
    
    // Toggle expand/collapse
    this.modifySymptomGroups[index].expanded = !wasExpanded;
    this.modifyHighlightedGroup = index;
  }

  selectModifySymptomGroup(index: number): void {
    this.modifyHighlightedGroup = index;
  }

  toggleModifySymptomInGroup(groupIndex: number, symptomId: number): void {
    const group = this.modifySymptomGroups[groupIndex];
    const index = group.selectedSymptoms.indexOf(symptomId);
    
    if (index > -1) {
      // Remove symptom
      group.selectedSymptoms = group.selectedSymptoms.filter(id => id !== symptomId);
    } else {
      // Add symptom
      if (group.allow_multiple) {
        group.selectedSymptoms.push(symptomId);
      } else {
        // Single selection - replace all
        group.selectedSymptoms = [symptomId];
      }
    }
  }

  isModifySymptomSelected(groupIndex: number, symptomId: number): boolean {
    return this.modifySymptomGroups[groupIndex].selectedSymptoms.includes(symptomId);
  }

  private resetModifyWizard(): void {
    this.clearPendingTimeout();
    this.modifyStep = 'search';
    this.modifyWizardError = null;
    this.modifySearch = '';
    this.selectedDisease = '';
    this.modifySymptomGroups = this.modifySymptomGroups.map(group => ({
      ...group,
      expanded: false,
      selectedSymptoms: []
    }));
    this.modifyHighlightedGroup = null;
  }

  // --- Helpers --------------------------------------------------------------

  private simulateAsync(callback: () => void): void {
    this.clearPendingTimeout();
    this.timeoutHandle = window.setTimeout(callback, 1400);
  }

  private clearPendingTimeout(): void {
    if (this.timeoutHandle) {
      window.clearTimeout(this.timeoutHandle);
      this.timeoutHandle = undefined;
    }
  }

  /**
   * Save disease with selected symptoms
   */
  private saveDiseaseWithSymptoms(): void {
    // Collect all selected symptom IDs
    const allSymptomIds: number[] = [];
    this.addSymptomGroups.forEach(group => {
      allSymptomIds.push(...group.selectedSymptoms);
    });

    if (allSymptomIds.length === 0) {
      this.addWizardError = 'Please select at least one symptom.';
      this.addStep = 'symptoms';
      return;
    }

    const payload = {
      disease_name: this.addDiseaseName.trim(),
      symptom_ids: allSymptomIds,
      recommendation: null // Can be added later if needed
    };

    this.apiService.post('/diseases/with-symptoms', payload).subscribe({
      next: (response) => {
        console.log('Disease saved successfully:', response);
        this.simulateAsync(() => {
          this.addStep = 'success';
        });
      },
      error: (error) => {
        console.error('Error saving disease:', error);
        this.addWizardError = error?.error?.detail || error?.message || 'Failed to save disease. Please try again.';
        this.addStep = 'symptoms';
      }
    });
  }

  /**
   * Search for disease and load its symptoms
   */
  private searchAndLoadDisease(diseaseName: string): void {
    this.modifyWizardError = null;
    const encodedName = encodeURIComponent(diseaseName);
    
    // First ensure symptom groups are loaded
    const loadGroupsPromise = this.modifySymptomGroups.length === 0
      ? new Promise<void>((resolve) => {
          this.predictionService.getGroupedSymptoms().subscribe({
            next: (response) => {
              this.modifySymptomGroups = response.groups.map(group => ({
                ...group,
                expanded: false,
                selectedSymptoms: []
              }));
              resolve();
            },
            error: () => resolve() // Continue even if groups fail to load
          });
        })
      : Promise.resolve();
    
    // Then search for disease
    loadGroupsPromise.then(() => {
      this.apiService.get(`/diseases/${encodedName}/symptoms`).subscribe({
        next: (response: any) => {
          console.log('Disease found:', response);
          this.selectedDisease = response.disease_name;
          
          // Pre-populate symptom groups with existing symptoms
          this.populateSymptomGroupsFromIds(response.symptom_ids);
          
          // Move to symptoms step
          this.modifyStep = 'symptoms';
        },
        error: (error) => {
          console.error('Error searching disease:', error);
          if (error?.status === 404) {
            this.modifyWizardError = `Disease "${diseaseName}" not found. Please check the name and try again.`;
          } else {
            this.modifyWizardError = error?.error?.detail || error?.message || 'Failed to search for disease. Please try again.';
          }
          this.modifyStep = 'search';
        }
      });
    });
  }

  /**
   * Populate symptom groups with selected symptom IDs
   */
  private populateSymptomGroupsFromIds(symptomIds: number[]): void {
    // Reset all selections
    this.modifySymptomGroups.forEach(group => {
      group.selectedSymptoms = [];
    });
    
    // Map symptom IDs to groups
    this.modifySymptomGroups.forEach((group, groupIndex) => {
      group.options.forEach(option => {
        if (symptomIds.includes(option.id)) {
          group.selectedSymptoms.push(option.id);
        }
      });
    });
  }

  /**
   * Update disease with selected symptoms
   */
  private updateDiseaseSymptoms(): void {
    // Collect all selected symptom IDs
    const allSymptomIds: number[] = [];
    this.modifySymptomGroups.forEach(group => {
      allSymptomIds.push(...group.selectedSymptoms);
    });

    if (allSymptomIds.length === 0) {
      this.modifyWizardError = 'Please select at least one symptom.';
      this.modifyStep = 'symptoms';
      return;
    }

    const payload = {
      symptom_ids: allSymptomIds,
      recommendation: null // Can be added later if needed
    };

    // URL encode disease name
    const encodedDiseaseName = encodeURIComponent(this.selectedDisease.trim());

    this.apiService.put(`/diseases/${encodedDiseaseName}/symptoms`, payload).subscribe({
      next: (response) => {
        console.log('Disease updated successfully:', response);
        this.simulateAsync(() => {
          this.modifyStep = 'success';
        });
      },
      error: (error) => {
        console.error('Error updating disease:', error);
        this.modifyWizardError = error?.error?.detail || error?.message || 'Failed to update disease. Please try again.';
        this.modifyStep = 'symptoms';
      }
    });
  }

  /**
   * Delete disease
   */
  confirmDeleteDisease(): void {
    this.showDeleteConfirmation = true;
  }

  cancelDelete(): void {
    this.showDeleteConfirmation = false;
  }

  deleteDisease(): void {
    if (!this.selectedDisease) {
      return;
    }

    this.isDeleting = true;
    this.modifyWizardError = null;
    const encodedName = encodeURIComponent(this.selectedDisease.trim());

    this.apiService.delete(`/diseases/by-name/${encodedName}`).subscribe({
      next: (response) => {
        console.log('Disease deleted successfully:', response);
        this.isDeleting = false;
        this.showDeleteConfirmation = false;
        this.closeModifyWizard();
        // Optionally show success message or refresh
      },
      error: (error) => {
        console.error('Error deleting disease:', error);
        this.isDeleting = false;
        this.showDeleteConfirmation = false;
        this.modifyWizardError = error?.error?.detail || error?.message || 'Failed to delete disease. Please try again.';
      }
    });
  }

  /**
   * Handle click outside to close expanded symptom groups
   */
  @HostListener('document:click', ['$event'])
  handleClickOutside(event: MouseEvent): void {
    // Check if click is outside symptom group containers and dropdowns
    const target = event.target as HTMLElement;
    
    // Close all expanded groups in add wizard if click is outside
    if (this.addWizardOpen) {
      const isClickInsideGroup = target.closest('.ds-tree__group-container');
      const isClickInsideDropdown = target.closest('.ds-tree__symptoms');
      const isClickOnGroupButton = target.closest('.ds-tree__node');
      
      // Only close if click is completely outside group container and not on group button
      if (!isClickInsideGroup && !isClickInsideDropdown && !isClickOnGroupButton) {
        this.addSymptomGroups.forEach(group => {
          group.expanded = false;
        });
      }
    }
    
    // Close all expanded groups in modify wizard if click is outside
    if (this.modifyWizardOpen) {
      const isClickInsideGroup = target.closest('.ds-tree__group-container');
      const isClickInsideDropdown = target.closest('.ds-tree__symptoms');
      const isClickOnGroupButton = target.closest('.ds-tree__node');
      
      // Only close if click is completely outside group container and not on group button
      if (!isClickInsideGroup && !isClickInsideDropdown && !isClickOnGroupButton) {
        this.modifySymptomGroups.forEach(group => {
          group.expanded = false;
        });
      }
    }
  }
}

