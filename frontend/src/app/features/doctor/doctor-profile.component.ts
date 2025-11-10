import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth.service';

/**
 * Doctor profile component
 */
@Component({
  selector: 'app-doctor-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './doctor-profile.component.html',
  styleUrls: ['./doctor-profile.component.scss']
})
export class DoctorProfileComponent {
  name = '';
  idNumber = '';
  showSuccess = false;

  constructor(private authService: AuthService) {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser?.name) {
      this.name = currentUser.name;
    }
  }

  saveProfile(): void {
    if (!this.name.trim() || !this.idNumber.trim()) {
      this.showSuccess = false;
      return;
    }
    this.showSuccess = true;
  }
}

