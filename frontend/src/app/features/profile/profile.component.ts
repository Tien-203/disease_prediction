import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="profile-page">
      <h1>Profile</h1>
      <p>Your personalised profile experience is coming soon.</p>
    </div>
  `,
  styles: [`
    .profile-page {
      min-height: calc(100vh - 160px);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background-color: #f5f9e9;
      color: #113226;
      gap: 16px;
      text-align: center;
    }
  `]
})
export class ProfileComponent {}


