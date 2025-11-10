import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

/**
 * Register Component
 */
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  name: string = '';
  age: number | null = null;
  gender: string = '';
  selectedRole: 'patient' | 'doctor' | 'researcher' | 'data_scientist' = 'patient';
  loading: boolean = false;
  error: string | null = null;
  showPassword: boolean = false;
  showConfirmPassword: boolean = false;
  readonly roles = [
    { value: 'patient', label: 'Patient' },
    { value: 'doctor', label: 'Doctor' },
    { value: 'researcher', label: 'Researcher' },
    { value: 'data_scientist', label: 'Data Scientist' }
  ];

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  /**
   * Toggle password visibility
   */
  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  /**
   * Toggle confirm password visibility
   */
  toggleConfirmPasswordVisibility() {
    this.showConfirmPassword = !this.showConfirmPassword;
  }

  /**
   * Handle form submission
   */
  onSubmit() {
    // Reset error
    this.error = null;

    // Validation
    if (!this.email || !this.password || !this.confirmPassword) {
      this.error = 'Please fill in all required fields';
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.error = 'Passwords do not match';
      return;
    }

    if (this.password.length < 6) {
      this.error = 'Password must be at least 6 characters long';
      return;
    }

    if (this.age !== null && (this.age < 0 || this.age > 150)) {
      this.error = 'Age must be between 0 and 150';
      return;
    }

    this.loading = true;

    const userData: any = {
      email: this.email,
      password: this.password,
      role: this.selectedRole
    };

    if (this.name) {
      userData.name = this.name;
    }

    if (this.age !== null) {
      userData.age = this.age;
    }

    if (this.gender) {
      userData.gender = this.gender;
    }

    this.authService.register(userData).subscribe({
      next: (response) => {
        this.loading = false;
        const roleFromResponse = response?.user?.role as typeof this.selectedRole | undefined;
        this.redirectToRole(roleFromResponse || this.selectedRole);
      },
      error: (err) => {
        this.loading = false;
        this.error = err.message || 'Registration failed. Please try again.';
      }
    });
  }

  private redirectToRole(role?: string | null) {
    switch (role) {
      case 'data_scientist':
        this.router.navigate(['/ds']);
        break;
      case 'doctor':
        this.router.navigate(['/doctor']);
        break;
      case 'researcher':
        this.router.navigate(['/researcher']);
        break;
      default:
        this.router.navigate(['/patient']);
        break;
    }
  }
}

