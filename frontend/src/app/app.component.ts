import { Component } from '@angular/core';
import { Router, RouterOutlet, NavigationEnd } from '@angular/router';
import { HeaderComponent } from './shared/components/header.component';
import { CommonModule } from '@angular/common';
import { filter } from 'rxjs/operators';

/**
 * Root App Component
 */
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, HeaderComponent],
  template: `
    <div class="app-container">
      <app-header *ngIf="showHeader"></app-header>
      <main class="main-content" [class.main-content--full]="!showHeader">
        <router-outlet></router-outlet>
      </main>
      <footer class="footer" *ngIf="showFooter">
        <div class="container">
          <p>&copy; 2025 Disease Prediction System. Educational Purpose Only.</p>
        </div>
      </footer>
    </div>
  `,
  styles: [`
    .app-container {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background-color: #f5f9e9;
    }

    .main-content {
      flex: 1;
      width: 100%;
    }

    .main-content--full {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .footer {
      background-color: #102d24;
      color: #dcede0;
      padding: 24px 0;
      text-align: center;
      border-top: 1px solid rgba(220, 237, 224, 0.2);
    }

    .footer p {
      margin: 0;
      font-size: 13px;
      letter-spacing: 0.3px;
    }
  `]
})
export class AppComponent {
  title = 'Disease Prediction System';
  showHeader = true;
  showFooter = true;

  constructor(private router: Router) {
    this.router.events.pipe(filter((event): event is NavigationEnd => event instanceof NavigationEnd)).subscribe(event => {
      const currentUrl = event.urlAfterRedirects;
      console.log('AppComponent - NavigationEnd event:', currentUrl);
      const hideLayoutRoutes = ['/login', '/register'];
      this.showHeader = !hideLayoutRoutes.includes(currentUrl);
      this.showFooter = this.showHeader;
      console.log('AppComponent - showHeader:', this.showHeader, 'showFooter:', this.showFooter);
    });
  }
}

