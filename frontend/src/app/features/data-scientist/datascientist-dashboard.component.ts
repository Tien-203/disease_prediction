import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth.service';

type AddWizardStep = 'name' | 'questions' | 'saving' | 'success';
type ModifyWizardStep = 'search' | 'questions' | 'saving' | 'success';

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
  readonly addStepOrder: AddWizardStep[] = ['name', 'questions', 'saving', 'success'];
  addDiseaseName = '';
  addWizardError: string | null = null;
  addQuestions: string[] = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6'];
  addHighlightedQuestion = 4;

  modifyWizardOpen = false;
  modifyStep: ModifyWizardStep = 'search';
  readonly modifyStepOrder: ModifyWizardStep[] = ['search', 'questions', 'saving', 'success'];
  modifyWizardError: string | null = null;
  modifySearch = '';
  selectedDisease = '';
  modifyQuestions: string[] = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6'];
  modifyHighlightedQuestion = 0;

  private timeoutHandle?: number;

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser?.name) {
      this.displayName = currentUser.name;
    } else if (currentUser?.email) {
      this.displayName = currentUser.email.split('@')[0];
    }
  }

  ngOnDestroy(): void {
    this.clearPendingTimeout();
  }

  // --- Add disease wizard --------------------------------------------------

  openAddWizard(): void {
    this.resetAddWizard();
    this.addWizardOpen = true;
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
        this.addStep = 'questions';
        break;
      case 'questions':
        this.addWizardError = null;
        this.addStep = 'saving';
        this.simulateAsync(() => {
          this.addStep = 'success';
        });
        break;
      case 'success':
        this.closeAddWizard();
        break;
      default:
        break;
    }
  }

  addNewQuestion(): void {
    const nextNumber = this.addQuestions.length + 1;
    const label = `Question ${nextNumber}`;
    this.addQuestions = [...this.addQuestions, label];
    this.addHighlightedQuestion = this.addQuestions.length - 1;
  }

  addModifyQuestion(): void {
    const nextNumber = this.modifyQuestions.length + 1;
    const label = `Question ${nextNumber}`;
    this.modifyQuestions = [...this.modifyQuestions, label];
    this.modifyHighlightedQuestion = this.modifyQuestions.length - 1;
  }

  selectAddQuestion(index: number): void {
    this.addHighlightedQuestion = index;
  }

  private resetAddWizard(): void {
    this.clearPendingTimeout();
    this.addStep = 'name';
    this.addDiseaseName = '';
    this.addWizardError = null;
    this.addQuestions = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6'];
    this.addHighlightedQuestion = 4;
  }

  // --- Modify disease wizard -----------------------------------------------

  openModifyWizard(): void {
    this.resetModifyWizard();
    this.modifyWizardOpen = true;
  }

  closeModifyWizard(): void {
    this.clearPendingTimeout();
    this.modifyWizardOpen = false;
  }

  continueModifyWizard(): void {
    switch (this.modifyStep) {
      case 'search':
        if (!this.modifySearch.trim()) {
          this.modifyWizardError = 'Please choose a disease to continue.';
          return;
        }
        this.modifyWizardError = null;
        this.selectedDisease = this.modifySearch.trim();
        this.modifyStep = 'questions';
        break;
      case 'questions':
        this.modifyWizardError = null;
        this.modifyStep = 'saving';
        this.simulateAsync(() => {
          this.modifyStep = 'success';
        });
        break;
      case 'success':
        this.closeModifyWizard();
        break;
      default:
        break;
    }
  }

  selectModifyQuestion(index: number): void {
    this.modifyHighlightedQuestion = index;
  }

  private resetModifyWizard(): void {
    this.clearPendingTimeout();
    this.modifyStep = 'search';
    this.modifyWizardError = null;
    this.modifySearch = '';
    this.selectedDisease = '';
    this.modifyQuestions = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6'];
    this.modifyHighlightedQuestion = 0;
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
}

