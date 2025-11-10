import { Component } from '@angular/core';

/**
 * About Component
 */
@Component({
  selector: 'app-about',
  standalone: true,
  imports: [],
  template: `
    <div class="about-container">
      <div class="text-container">
        <h1 class="heading">About</h1>
        <p class="paragraph">
          This Symptom-Based Disease Prediction Application is an educational tool that uses 
          machine learning to predict possible diseases based on symptoms.
        </p>
        <p class="paragraph">
          The application uses a Random Forest classifier trained on medical data to provide 
          predictions with confidence scores. Please note that this is for educational purposes 
          only and should not replace professional medical advice.
        </p>
      </div>
    </div>
  `,
  styles: [`
    .about-container {
      padding: 0;
      max-width: 1440px;
      margin: 0 auto;
      min-height: calc(100vh - 85px);
    }

    .text-container {
      padding: 80px;
      max-width: 800px;
    }

    .heading {
      font-size: 48px;
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 30px;
      color: #333333;
    }

    .paragraph {
      font-size: 18px;
      line-height: 1.6;
      color: #666666;
      margin-bottom: 20px;
    }

    @media (max-width: 768px) {
      .text-container {
        padding: 40px 20px;
      }

      .heading {
        font-size: 36px;
      }

      .paragraph {
        font-size: 16px;
      }
    }
  `]
})
export class AboutComponent {
}

