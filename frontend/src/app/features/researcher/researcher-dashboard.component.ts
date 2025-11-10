import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';
import { Router } from '@angular/router';

/**
 * Researcher dashboard component
 */
@Component({
  selector: 'app-researcher-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './researcher-dashboard.component.html',
  styleUrls: ['./researcher-dashboard.component.scss']
})
export class ResearcherDashboardComponent implements OnInit {
  displayName = 'Researcher';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser?.name) {
      this.displayName = currentUser.name;
    } else if (currentUser?.email) {
      this.displayName = currentUser.email.split('@')[0];
    }
  }

  exportDataset(): void {
    this.router.navigate(['/researcher/dataset'], { queryParams: { action: 'export' } });
  }

  viewDataset(): void {
    this.router.navigate(['/researcher/dataset']);
  }
}

