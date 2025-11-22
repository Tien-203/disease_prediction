import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { User } from '../../../core/models/user.model';
import { RoleDisplayPipe } from '../../pipes/role-display.pipe';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatDividerModule } from '@angular/material/divider';

/**
 * Header component with navigation
 */
@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatMenuModule,
    MatDividerModule,
    RoleDisplayPipe
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent implements OnInit {
  currentUser: User | null = null;

  constructor(
    public authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }

  /**
   * Get navigation items based on user role
   */
  getNavigationItems(): { label: string; route: string; icon: string }[] {
    if (!this.currentUser) {
      return [];
    }

    switch (this.currentUser.role) {
      case 'patient':
        return [
          { label: 'Predict', route: '/patient/predict', icon: 'search' },
          { label: 'History', route: '/patient/history', icon: 'history' }
        ];
      case 'doctor':
        return [
          { label: 'Dashboard', route: '/doctor/dashboard', icon: 'dashboard' },
          { label: 'Patients', route: '/doctor/patients', icon: 'people' }
        ];
      case 'data_scientist':
        return [
          { label: 'Dashboard', route: '/data-scientist/dashboard', icon: 'dashboard' },
          { label: 'Model Info', route: '/data-scientist/model-info', icon: 'science' }
        ];
      case 'researcher':
        return [
          { label: 'Dashboard', route: '/researcher/dashboard', icon: 'dashboard' },
          { label: 'Statistics', route: '/researcher/statistics', icon: 'bar_chart' }
        ];
      default:
        return [];
    }
  }

  /**
   * Logout user
   */
  logout(): void {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }
}
