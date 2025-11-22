import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { LoggerService } from '../../../core/services/logger.service';
import { ErrorHandlerService } from '../../../core/services/error-handler.service';
import { UserRole } from '../../../core/models/user.model';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';

/**
 * Register component
 */
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatIconModule
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {
  registerForm: FormGroup;
  hidePassword = true;
  errorMessage = '';
  isLoading = false;
  roles: UserRole[] = ['patient', 'doctor', 'researcher', 'data_scientist'];

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private logger: LoggerService,
    private errorHandler: ErrorHandlerService
  ) {
    this.registerForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]],
      name: [''],
      age: ['', [Validators.min(0), Validators.max(150)]],
      gender: [''],
      role: ['patient', Validators.required]
    }, { validators: this.passwordMatchValidator });
  }

  /**
   * Custom validator to check if passwords match
   */
  passwordMatchValidator(group: FormGroup): { [key: string]: boolean } | null {
    const password = group.get('password');
    const confirmPassword = group.get('confirmPassword');
    
    if (password && confirmPassword && password.value !== confirmPassword.value) {
      return { passwordMismatch: true };
    }
    
    return null;
  }

  /**
   * Handle form submission
   */
  onSubmit(): void {
    if (this.registerForm.valid) {
      this.isLoading = true;
      this.errorMessage = '';

      const userData = {
        email: this.registerForm.value.email,
        password: this.registerForm.value.password,
        name: this.registerForm.value.name || undefined,
        age: this.registerForm.value.age ? parseInt(this.registerForm.value.age) : undefined,
        gender: this.registerForm.value.gender || undefined,
        role: this.registerForm.value.role
      };

      this.authService.register(userData).subscribe({
        next: () => {
          this.logger.info('Registration successful');
          const user = this.authService.getCurrentUser();
          const defaultRoute = user?.role === 'patient' ? '/patient/predict' : '/';
          this.router.navigate([defaultRoute]);
        },
        error: (error) => {
          this.errorMessage = this.errorHandler.handleError(error);
          this.isLoading = false;
        }
      });
    }
  }

  /**
   * Navigate to login page
   */
  navigateToLogin(): void {
    this.router.navigate(['/auth/login']);
  }
}
