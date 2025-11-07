import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './shared/components/header.component';

/**
 * Root App Component
 */
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HeaderComponent],
  template: `
    <div class="app-container">
      <app-header></app-header>
      <main class="main-content">
        <router-outlet></router-outlet>
      </main>
      <footer class="footer">
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
    }

    .main-content {
      flex: 1;
    }

    .footer {
      background-color: #333;
      color: white;
      padding: 20px 0;
      text-align: center;
      margin-top: 40px;
    }

    .footer p {
      margin: 0;
    }
  `]
})
export class AppComponent {
  title = 'Disease Prediction System';
}

