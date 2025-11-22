import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { SymptomService, Symptom } from '../../../features/services/symptom.service';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatInputModule } from '@angular/material/input';
import { Observable, startWith, map } from 'rxjs';

/**
 * Reusable symptom selector component
 */
@Component({
  selector: 'app-symptom-selector',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatChipsModule,
    MatIconModule,
    MatAutocompleteModule,
    MatInputModule
  ],
  templateUrl: './symptom-selector.component.html',
  styleUrl: './symptom-selector.component.scss'
})
export class SymptomSelectorComponent implements OnInit {
  @Input() selectedSymptoms: string[] = [];
  @Output() symptomsChange = new EventEmitter<string[]>();

  symptoms: Symptom[] = [];
  filteredSymptoms$!: Observable<Symptom[]>;
  symptomControl = new FormControl('');
  selectedSymptomNames: string[] = [];

  constructor(private symptomService: SymptomService) {}

  ngOnInit(): void {
    this.loadSymptoms();
    this.selectedSymptomNames = [...this.selectedSymptoms];
    
    this.filteredSymptoms$ = this.symptomControl.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value || ''))
    );
  }

  /**
   * Load all symptoms from API
   */
  loadSymptoms(): void {
    this.symptomService.getSymptoms(0, 1000).subscribe({
      next: (response) => {
        this.symptoms = response.symptoms;
      },
      error: (error) => {
        console.error('Error loading symptoms:', error);
      }
    });
  }

  /**
   * Filter symptoms based on search input
   */
  private _filter(value: string): Symptom[] {
    const filterValue = value.toLowerCase();
    return this.symptoms.filter(symptom => 
      symptom.name.toLowerCase().includes(filterValue) &&
      !this.selectedSymptomNames.includes(symptom.name)
    );
  }

  /**
   * Add symptom to selection
   */
  addSymptom(symptomName: string): void {
    if (symptomName && !this.selectedSymptomNames.includes(symptomName)) {
      this.selectedSymptomNames.push(symptomName);
      this.symptomsChange.emit([...this.selectedSymptomNames]);
      this.symptomControl.setValue('');
    }
  }

  /**
   * Remove symptom from selection
   */
  removeSymptom(symptomName: string): void {
    const index = this.selectedSymptomNames.indexOf(symptomName);
    if (index >= 0) {
      this.selectedSymptomNames.splice(index, 1);
      this.symptomsChange.emit([...this.selectedSymptomNames]);
    }
  }

  /**
   * Handle option selection from autocomplete
   */
  onOptionSelected(event: any): void {
    const symptomName = event.option.value;
    if (typeof symptomName === 'string') {
      this.addSymptom(symptomName);
    }
  }
}
