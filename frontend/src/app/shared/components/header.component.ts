import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { environment } from '../../../environments/environment';

/**
 * Header Component
 */
@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  template: `
    <header class="header">
      <div class="container">
        <nav class="nav">
          <div class="logo">
            <h2>🏥 {{ appName }}</h2>
          </div>
          <ul class="nav-links">
            <li><a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">Home</a></li>
            <li><a routerLink="/prediction" routerLinkActive="active">Prediction</a></li>
          </ul>
        </nav>
      </div>
    </header>
  `,
  styles: [`
    .header {
      background-color: #4CAF50;
      color: white;
      padding: 1rem 0;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .logo h2 {
      margin: 0;
      font-size: 24px;
    }

    .nav-links {
      display: flex;
      list-style: none;
      gap: 30px;
      margin: 0;
    }

    .nav-links a {
      color: white;
      text-decoration: none;
      font-size: 16px;
      font-weight: 500;
      padding: 8px 16px;
      border-radius: 4px;
      transition: background-color 0.3s;
    }

    .nav-links a:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }

    .nav-links a.active {
      background-color: rgba(255, 255, 255, 0.2);
    }
  `]
})
export class HeaderComponent {
  appName = environment.appName;
}

