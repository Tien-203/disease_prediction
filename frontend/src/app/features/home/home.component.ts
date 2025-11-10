import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth.service';
import { PredictionService } from '../prediction/services/prediction.service';
import { Symptom } from '../prediction/models/symptom.model';
import { PredictionResponse, DiseaseInfo } from '../prediction/models/prediction.model';
import { finalize } from 'rxjs/operators';

type QuickCheckStep = 1 | 2 | 3 | 4;

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  userName: string = 'Patient';

  quickCheckVisible = false;
  quickCheckStep: QuickCheckStep = 1;
  quickCheckError: string | null = null;

  describeModalOpen = false;
  describeText: string = '';
  describeError: string | null = null;

  symptomsLoading = false;
  allSymptoms: Symptom[] = [];
  selectedSymptoms: string[] = [];
  symptomSearch: string = '';

  questionAnswers: string[] = ['', '', '', ''];
  readonly questionPrompts: string[] = [
    'How long have you experienced these symptoms?',
    'Do you have any existing medical conditions?',
    'Are you currently taking any medication?',
    'Have you noticed anything that improves or worsens the symptoms?'
  ];

  isPredicting = false;
  predictionResult: PredictionResponse | null = null;

  readonly stepLabels = ['1', '2', '3', '4'];

  constructor(
    private authService: AuthService,
    private predictionService: PredictionService
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

    this.loadSymptoms();
  }

  get filteredSymptoms(): Symptom[] {
    const search = this.symptomSearch.trim().toLowerCase();
    if (!search) {
      return this.allSymptoms.slice(0, 6);
    }

    return this.allSymptoms
      .filter((symptom) =>
        symptom.name.toLowerCase().includes(search) ||
        symptom.description?.toLowerCase().includes(search)
      )
      .slice(0, 8);
  }

  startQuickCheck(): void {
    this.quickCheckVisible = true;
    this.quickCheckStep = 1;
    this.quickCheckError = null;
    this.predictionResult = null;
    this.questionAnswers = ['', '', '', ''];
    this.selectedSymptoms = [];
    this.symptomSearch = '';
  }

  closeQuickCheck(): void {
    this.quickCheckVisible = false;
    this.quickCheckError = null;
    this.predictionResult = null;
    this.isPredicting = false;
    this.selectedSymptoms = [];
    this.symptomSearch = '';
  }

  loadSymptoms(): void {
    this.symptomsLoading = true;
    this.predictionService.getSymptoms(0, 200).pipe(
      finalize(() => this.symptomsLoading = false)
    ).subscribe({
      next: (response) => {
        this.allSymptoms = response.symptoms;
      },
      error: () => {
        this.quickCheckError = 'Unable to load symptom list right now. Please try again later.';
      }
    });
  }

  addSymptom(symptomName: string): void {
    const trimmed = symptomName.trim();
    if (!trimmed) {
      return;
    }

    if (!this.selectedSymptoms.includes(trimmed)) {
      this.selectedSymptoms = [...this.selectedSymptoms, trimmed];
    }
    this.symptomSearch = '';
  }

  removeSymptom(symptomName: string): void {
    this.selectedSymptoms = this.selectedSymptoms.filter(item => item !== symptomName);
  }

  handleSymptomEnter(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      event.preventDefault();
      this.addSymptom(this.symptomSearch);
    }
  }

  goToQuestions(): void {
    if (this.selectedSymptoms.length === 0) {
      this.quickCheckError = 'Please add at least one symptom to continue.';
      return;
    }

    this.quickCheckError = null;
    this.quickCheckStep = 2;
  }

  submitQuickCheck(): void {
    if (this.selectedSymptoms.length === 0) {
      this.quickCheckError = 'Please make sure you selected at least one symptom.';
      this.quickCheckStep = 1;
      return;
    }

    this.runPrediction(this.selectedSymptoms);
  }

  runPrediction(symptoms: string[]): void {
    this.isPredicting = true;
    this.quickCheckError = null;
    this.predictionResult = null;
    this.quickCheckStep = 3;

    this.predictionService.predictDisease({ symptoms }).pipe(
      finalize(() => this.isPredicting = false)
    ).subscribe({
      next: (response) => {
        this.predictionResult = response;
        this.quickCheckStep = 4;
      },
      error: () => {
        this.quickCheckError = 'We could not process your symptoms right now. Please try again.';
        this.quickCheckStep = 1;
      }
    });
  }

  openDescribeModal(): void {
    this.describeModalOpen = true;
    this.describeError = null;
    this.describeText = '';
  }

  closeDescribeModal(): void {
    this.describeModalOpen = false;
    this.describeError = null;
    this.describeText = '';
  }

  submitFeelingDescription(): void {
    const description = this.describeText.trim();
    if (!description) {
      this.describeError = 'Please describe how you feel before continuing.';
      return;
    }

    const potentialSymptoms = description
      .split(/,|;|\n/)
      .map(part => part.trim())
      .filter(Boolean);

    if (potentialSymptoms.length === 0) {
      this.describeError = 'Try separating symptoms with commas so we can understand them.';
      return;
    }

    this.closeDescribeModal();
    this.selectedSymptoms = potentialSymptoms;
    this.quickCheckVisible = true;
    this.runPrediction(this.selectedSymptoms);
  }

  getConfidencePercentage(confidence: number | undefined): number {
    if (!confidence && confidence !== 0) {
      return 0;
    }
    return Math.round(confidence * 100);
  }

  getRecommendationList(info?: DiseaseInfo): string[] {
    if (!info) {
      return [];
    }

    if (info.precautions && info.precautions.length > 0) {
      return info.precautions;
    }

    if (info.recommendations) {
      return info.recommendations
        .split(/\.|\n|;/)
        .map(item => item.trim())
        .filter(Boolean);
    }

    return [];
  }
}
