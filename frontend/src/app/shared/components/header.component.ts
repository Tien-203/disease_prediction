import { Component, OnDestroy, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { AuthService } from '../../core/services/auth.service';

interface NavLink {
  label: string;
  path: string;
  exact?: boolean;
}

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, CommonModule],
  template: `
    <header class="app-header">
      <div class="app-header__inner">
        <div class="app-header__brand">
          <span class="app-header__logo">Symptom-Based Disease Prediction</span>
        </div>

        <ng-container *ngIf="isAuthenticated; else guestNav">
          <nav class="app-header__nav">
            <a
              *ngFor="let link of navLinks"
              [routerLink]="link.path"
              routerLinkActive="app-header__link--active"
              [routerLinkActiveOptions]="link.exact ? exactMatch : defaultMatch"
              class="app-header__link"
            >
              {{ link.label }}
            </a>
            <button type="button" class="app-header__logout" (click)="logout()">
              Log Out
            </button>
          </nav>
        </ng-container>

        <ng-template #guestNav>
          <div class="app-header__guest">
            <a routerLink="/login" class="app-header__link app-header__link--guest">
              Login
            </a>
          </div>
        </ng-template>
      </div>
    </header>
  `,
  styles: [`
    .app-header {
      width: 100%;
      background-color: #102d24;
      color: #f4f9ee;
      padding: 20px 48px;
      box-shadow: 0 6px 16px rgba(16, 45, 36, 0.25);
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .app-header__inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      max-width: 1200px;
      margin: 0 auto;
      width: 100%;
    }

    .app-header__brand {
      flex: 1;
    }

    .app-header__logo {
      font-size: 18px;
      font-weight: 600;
      letter-spacing: 0.5px;
    }

    .app-header__nav {
      display: flex;
      align-items: center;
      gap: 28px;
    }

    .app-header__link {
      color: #dcede0;
      text-decoration: none;
      font-size: 15px;
      font-weight: 500;
      position: relative;
      transition: color 0.2s ease;
      padding: 4px 0;
    }

    .app-header__link::after {
      content: '';
      position: absolute;
      left: 0;
      bottom: -6px;
      width: 0;
      height: 3px;
      border-radius: 999px;
      background-color: #c9ea74;
      transition: width 0.2s ease;
    }

    .app-header__link:hover::after,
    .app-header__link--active::after {
      width: 100%;
    }

    .app-header__link:hover,
    .app-header__link--active {
      color: #f4f9ee;
    }

    .app-header__logout {
      border: none;
      border-radius: 16px;
      padding: 10px 24px;
      background-color: #c9ea74;
      color: #102d24;
      font-weight: 600;
      font-size: 14px;
      cursor: pointer;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
      box-shadow: 0 10px 20px rgba(201, 234, 116, 0.25);
    }

    .app-header__logout:hover {
      transform: translateY(-1px);
      box-shadow: 0 14px 24px rgba(201, 234, 116, 0.35);
    }

    .app-header__guest .app-header__link {
      font-size: 16px;
    }

    .app-header__link--guest::after {
      display: none;
    }

    @media (max-width: 768px) {
      .app-header {
        padding: 16px 24px;
      }

      .app-header__inner {
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
      }

      .app-header__nav {
        width: 100%;
        flex-wrap: wrap;
        gap: 18px;
      }
    }
  `]
})
export class HeaderComponent implements OnInit, OnDestroy {
  isAuthenticated = false;
  currentUser: { role?: string; name?: string } | null = null;

  readonly exactMatch = { exact: true as const };
  readonly defaultMatch = { exact: false as const };

  private subscription?: Subscription;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.subscription = this.authService.isAuthenticated$.subscribe(isAuth => {
      this.isAuthenticated = isAuth;
      this.currentUser = isAuth ? this.authService.getCurrentUser() : null;
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  get navLinks(): NavLink[] {
    if (!this.isAuthenticated) {
      return [];
    }

    switch (this.currentUser?.role) {
      case 'researcher':
        return [
          { label: 'Home', path: '/researcher', exact: true },
          { label: 'Profile', path: '/researcher/profile' },
          { label: 'Dataset', path: '/researcher/dataset' }
        ];
      case 'doctor':
        return [
          { label: 'Home', path: '/doctor', exact: true },
          { label: 'Profile', path: '/doctor/profile' },
          { label: 'Dataset', path: '/doctor/dataset' },
          { label: 'Patient', path: '/doctor/patients' }
        ];
      case 'data_scientist':
        return [
          { label: 'Home', path: '/ds', exact: true },
          { label: 'Profile', path: '/ds/profile' },
          { label: 'Dataset', path: '/ds/dataset' }
        ];
      default:
        return [
          { label: 'Home', path: '/patient', exact: true },
          { label: 'Profile', path: '/profile' },
          { label: 'History', path: '/history' }
        ];
    }
  }

  logout() {
    this.authService.logout();
  }
}
