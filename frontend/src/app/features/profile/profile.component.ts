import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth.service';

/**
 * Profile Component
 * Displays and allows editing of user personal information
 */
@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  name: string = '';
  age: number | null = null;
  gender: string = '';
  
  loading: boolean = false;
  saving: boolean = false;
  error: string | null = null;
  success: string | null = null;

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.loadProfile();
  }

  /**
   * Load user profile data
   */
  loadProfile(): void {
    // First try to load from localStorage (faster)
    const currentUser = this.authService.getCurrentUser();
    if (currentUser) {
      this.name = currentUser.name || '';
      this.age = currentUser.age || null;
      this.gender = currentUser.gender || '';
    }

    // Then fetch from API to get latest data
    this.loading = true;
    this.error = null;
    
    this.authService.getProfile().subscribe({
      next: (user) => {
        this.name = user.name || '';
        this.age = user.age || null;
        this.gender = user.gender || '';
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading profile:', err);
        // If API fails but we have localStorage data, keep using it
        if (!currentUser) {
          this.error = err.message || 'Failed to load profile';
        }
        this.loading = false;
      }
    });
  }

  /**
   * Handle form submission
   */
  onSubmit(): void {
    this.error = null;
    this.success = null;

    // Validation
    if (this.age !== null && (this.age < 0 || this.age > 150)) {
      this.error = 'Age must be between 0 and 150';
      return;
    }

    this.saving = true;

    const profileData: any = {};
    if (this.name) {
      profileData.name = this.name;
    }
    if (this.age !== null) {
      profileData.age = this.age;
    }
    if (this.gender) {
      profileData.gender = this.gender;
    }

    this.authService.updateProfile(profileData).subscribe({
      next: () => {
        this.saving = false;
        this.success = 'Profile updated successfully!';
        // Clear success message after 3 seconds
        setTimeout(() => {
          this.success = null;
        }, 3000);
      },
      error: (err) => {
        this.saving = false;
        this.error = err.message || 'Failed to update profile';
      }
    });
  }

  /**
   * Handle gender selection
   */
  selectGender(gender: string): void {
    this.gender = gender;
  }
}
