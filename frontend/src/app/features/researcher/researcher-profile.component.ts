import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth.service';

/**
 * Researcher profile component
 */
@Component({
  selector: 'app-researcher-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './researcher-profile.component.html',
  styleUrls: ['./researcher-profile.component.scss']
})
export class ResearcherProfileComponent implements OnInit {
  name = '';
  idNumber = '';
  loading = false;
  saving = false;
  error: string | null = null;
  success: string | null = null;

  // Key for storing ID number in localStorage
  private readonly ID_NUMBER_KEY = 'researcher_id_number';

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.loadProfile();
  }

  /**
   * Load user profile data from localStorage and API
   */
  loadProfile(): void {
    // Load from localStorage first
    const currentUser = this.authService.getCurrentUser();
    if (currentUser) {
      this.name = currentUser.name || '';
    }

    // Load ID number from localStorage
    const storedIdNumber = localStorage.getItem(this.ID_NUMBER_KEY);
    if (storedIdNumber) {
      this.idNumber = storedIdNumber;
    }

    // Optionally try to fetch from API
    this.loading = true;
    this.authService.getProfile().subscribe({
      next: (user) => {
        if (user && user.name) {
          this.name = user.name;
        }
        this.loading = false;
      },
      error: (err) => {
        // Silently fail - just use localStorage data
        console.log('API not available, using localStorage data');
        this.loading = false;
      }
    });
  }

  /**
   * Save profile data to localStorage and optionally to API
   */
  saveProfile(): void {
    // Reset messages
    this.error = null;
    this.success = null;

    // Validation
    if (!this.name.trim()) {
      this.error = 'Researcher Name is required';
      return;
    }

    if (!this.idNumber.trim()) {
      this.error = 'ID Number is required';
      return;
    }

    this.saving = true;

    // Update localStorage immediately
    const currentUser = this.authService.getCurrentUser();
    if (currentUser) {
      currentUser.name = this.name.trim();
      localStorage.setItem('user_data', JSON.stringify(currentUser));
    }

    // Save ID number to localStorage
    localStorage.setItem(this.ID_NUMBER_KEY, this.idNumber.trim());

    // Try to update via API
    const profileData: { name?: string } = {
      name: this.name.trim()
    };

    this.authService.updateProfile(profileData).subscribe({
      next: () => {
        this.saving = false;
        this.success = 'Profile updated successfully!';
        setTimeout(() => {
          this.success = null;
        }, 3000);
      },
      error: (err) => {
        // Still show success since we saved to localStorage
        console.log('API update failed, but saved to localStorage');
        this.saving = false;
        this.success = 'Profile saved successfully!';
        setTimeout(() => {
          this.success = null;
        }, 3000);
      }
    });
  }
}

