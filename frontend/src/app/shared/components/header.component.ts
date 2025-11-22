import { Component, OnDestroy, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { AuthService } from '../../core/services/auth.service';
import { environment } from '../../../environments/environment';
import { NavLink, ROLE_NAV_LINKS, getHomeRouteForRole } from '../../core/config/routes.config';
import { NzDropDownModule } from 'ng-zorro-antd/dropdown';
import { NzButtonModule } from 'ng-zorro-antd/button';

/**
 * Header Component
 * Main navigation header with role-based menu using Bootstrap 5 and Ant Design
 */
@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, CommonModule, NzDropDownModule, NzButtonModule],
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

  // Role switcher
  showRoleSwitcher = false;
  readonly availableRoles: Array<{ value: 'patient' | 'doctor' | 'researcher' | 'data_scientist'; label: string; icon: string }> = [
    { value: 'patient', label: 'Patient', icon: '👤' },
    { value: 'doctor', label: 'Doctor', icon: '👨‍⚕️' },
    { value: 'researcher', label: 'Researcher', icon: '🔬' },
    { value: 'data_scientist', label: 'Data Scientist', icon: '📊' }
  ];

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

    const normalizedRole = this.normalizeRole(this.currentUser.role);
    return ROLE_NAV_LINKS[normalizedRole] || ROLE_NAV_LINKS['patient'];
  }

  /**
   * Get home route for the current user
   */
  get homeRoute(): string {
    return getHomeRouteForRole(this.currentUser?.role);
  }

  /**
   * Toggle role switcher dropdown
   */
  toggleRoleSwitcher(): void {
    this.showRoleSwitcher = !this.showRoleSwitcher;
  }

  /**
   * Switch to a different role
   */
  switchRole(role: 'patient' | 'doctor' | 'researcher' | 'data_scientist'): void {
    this.authService.switchRole(role);
    this.showRoleSwitcher = false;
  }

  /**
   * Get current role display name
   */
  get currentRoleDisplay(): string {
    const role = this.normalizeRole(this.currentUser?.role);
    const roleObj = this.availableRoles.find(r => r.value === role);
    return roleObj ? `${roleObj.icon} ${roleObj.label}` : '👤 User';
  }

  /**
   * Normalize role string
   */
  normalizeRole(role?: string): string {
    if (!role) return 'patient';
    return role.toLowerCase().replace(/\s+/g, '_');
  }

  /**
   * Check if a role is currently active
   */
  isRoleActive(roleValue: string): boolean {
    const currentRole = this.normalizeRole(this.currentUser?.role);
    return currentRole === roleValue;
  }

  /**
   * Logout user
   */
  logout(): void {
    this.authService.logout();
  }
}
