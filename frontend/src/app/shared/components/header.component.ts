import { Component, OnDestroy, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { AuthService } from '../../core/services/auth.service';
import { environment } from '../../../environments/environment';
import { NavLink, ROLE_NAV_LINKS, getHomeRouteForRole } from '../../core/config/routes.config';

/**
 * Header Component
 * Main navigation header with role-based menu
 */
@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, CommonModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, OnDestroy {
  // App configuration
  readonly appName = environment.appName;

  // Authentication state
  isAuthenticated = false;
  currentUser: { role?: string; name?: string } | null = null;

  // Router link options
  readonly exactMatch = { exact: true as const };
  readonly defaultMatch = { exact: false as const };

  private subscription?: Subscription;

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.subscription = this.authService.isAuthenticated$.subscribe(isAuth => {
      this.isAuthenticated = isAuth;
      this.currentUser = isAuth ? this.authService.getCurrentUser() : null;
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  /**
   * Get navigation links based on user role
   */
  get navLinks(): NavLink[] {
    if (!this.isAuthenticated || !this.currentUser?.role) {
      return [];
    }

    const normalizedRole = this.currentUser.role.toLowerCase().replace(/\s+/g, '_');
    return ROLE_NAV_LINKS[normalizedRole] || ROLE_NAV_LINKS['patient'];
  }

  /**
   * Get home route for the current user
   */
  get homeRoute(): string {
    return getHomeRouteForRole(this.currentUser?.role);
  }

  /**
   * Logout user
   */
  logout(): void {
    this.authService.logout();
  }
}
