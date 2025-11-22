import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
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
 * Login component
 */
@Component({
  selector: 'app-login',
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
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  loginForm: FormGroup;
  hidePassword = true;
  errorMessage = '';
  isLoading = false;
  roles: UserRole[] = ['patient', 'doctor', 'researcher', 'data_scientist'];

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private logger: LoggerService,
    private errorHandler: ErrorHandlerService
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      role: ['']
    });
  }

  /**
   * Handle form submission
   */
  onSubmit(): void {
    if (this.loginForm.valid) {
      this.isLoading = true;
      this.errorMessage = '';

      const credentials = {
        email: this.loginForm.value.email,
        password: this.loginForm.value.password,
        role: this.loginForm.value.role || undefined
      };

      this.authService.login(credentials).subscribe({
        next: () => {
          this.logger.info('Login successful');
          const returnUrl = this.route.snapshot.queryParams['returnUrl'] || this.getDefaultRoute();
          this.router.navigate([returnUrl]);
        },
        error: (error) => {
          this.errorMessage = this.errorHandler.handleError(error);
          this.isLoading = false;
        }
      });
    }
  }

  /**
   * Get default route based on user role
   */
  private getDefaultRoute(): string {
    const user = this.authService.getCurrentUser();
    if (!user) return '/';

    switch (user.role) {
      case 'patient':
        return '/patient/predict';
      case 'doctor':
        return '/doctor/dashboard';
      case 'data_scientist':
        return '/data-scientist/dashboard';
      case 'researcher':
        return '/researcher/dashboard';
      default:
        return '/';
    }
  }

  /**
   * Navigate to register page
   */
  navigateToRegister(): void {
    this.router.navigate(['/auth/register']);
  }
}
