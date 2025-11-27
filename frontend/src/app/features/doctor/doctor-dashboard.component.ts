import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';
import { Router } from '@angular/router';

/**
 * Doctor dashboard component
 */
@Component({
  selector: 'app-doctor-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './doctor-dashboard.component.html',
  styleUrls: ['./doctor-dashboard.component.scss']
})
export class DoctorDashboardComponent implements OnInit {
  displayName = 'Doctor';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser?.name) {
      this.displayName = currentUser.name;
    } else if (currentUser?.email) {
      this.displayName = currentUser.email;
    }
  }

  goToPatients(): void {
    this.router.navigate(['/doctor/patients']);
  }

  goToDataset(): void {
    this.router.navigate(['/doctor/dataset']);
  }
}

