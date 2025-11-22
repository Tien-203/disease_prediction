import { Component } from '@angular/core';
import { Router, RouterOutlet, NavigationEnd } from '@angular/router';
import { HeaderComponent } from './shared/components/header.component';
import { CommonModule } from '@angular/common';
import { filter } from 'rxjs/operators';
import { environment } from '../environments/environment';
import { HIDE_LAYOUT_ROUTES } from './core/config/routes.config';

/**
 * Root App Component
 */
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, HeaderComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  // Configuration from environment
  readonly appName = environment.appName;
  readonly appVersion = environment.version;

  // Dynamic footer text
  get footerText(): string {
    const currentYear = new Date().getFullYear();
    return `© ${currentYear} ${this.appName}. Educational Purpose Only.`;
  }

  // Layout visibility
  showHeader = true;
  showFooter = true;

  constructor(private router: Router) {
    this.initializeLayoutToggle();
  }

  /**
   * Initialize layout visibility based on route
   */
  private initializeLayoutToggle(): void {
    this.router.events
      .pipe(filter((event): event is NavigationEnd => event instanceof NavigationEnd))
      .subscribe(event => {
        const currentUrl = event.urlAfterRedirects;
        this.updateLayoutVisibility(currentUrl);
      });
  }

  /**
   * Update header and footer visibility based on current route
   */
  private updateLayoutVisibility(url: string): void {
    const shouldHideLayout = HIDE_LAYOUT_ROUTES.some(route => url.startsWith(route));
    this.showHeader = !shouldHideLayout;
    this.showFooter = !shouldHideLayout;
  }
}

