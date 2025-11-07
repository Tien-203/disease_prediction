import { Component } from '@angular/core';
import { Router } from '@angular/router';

/**
 * Home Component
 */
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  template: `
    <div class="home-container">
      <div class="hero">
        <h1>🏥 Disease Prediction System</h1>
        <p class="subtitle">Predict diseases based on symptoms using Machine Learning</p>
        <button class="btn btn-primary btn-large" (click)="goToPrediction()">
          Start Prediction
        </button>
      </div>

      <div class="features">
        <div class="feature-card">
          <div class="feature-icon">🤖</div>
          <h3>ML Powered</h3>
          <p>Uses Random Forest algorithm for accurate predictions</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>Confidence Scores</h3>
          <p>Get prediction confidence levels and alternative diagnoses</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">💊</div>
          <h3>Disease Information</h3>
          <p>Receive detailed information and precautions for each disease</p>
        </div>
      </div>

      <div class="info-section">
        <h2>How It Works</h2>
        <div class="steps">
          <div class="step">
            <span class="step-number">1</span>
            <h4>Select Symptoms</h4>
            <p>Choose the symptoms you're experiencing from the list</p>
          </div>
          <div class="step">
            <span class="step-number">2</span>
            <h4>Get Prediction</h4>
            <p>Our ML model analyzes your symptoms and predicts possible diseases</p>
          </div>
          <div class="step">
            <span class="step-number">3</span>
            <h4>View Results</h4>
            <p>See prediction results with confidence scores and recommendations</p>
          </div>
        </div>
      </div>

      <div class="disclaimer">
        <p><strong>⚠️ Disclaimer:</strong> This is an educational tool and should not be used as a substitute for professional medical advice. Always consult with a qualified healthcare provider for medical concerns.</p>
      </div>
    </div>
  `,
  styles: [`
    .home-container {
      padding: 40px 20px;
      max-width: 1200px;
      margin: 0 auto;
    }

    .hero {
      text-align: center;
      padding: 60px 20px;
      background: white;
      border-radius: 12px;
      margin-bottom: 40px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .hero h1 {
      font-size: 48px;
      margin-bottom: 20px;
      color: #333;
    }

    .subtitle {
      font-size: 20px;
      color: #666;
      margin-bottom: 30px;
    }

    .btn-large {
      padding: 16px 40px;
      font-size: 18px;
    }

    .features {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 30px;
      margin-bottom: 60px;
    }

    .feature-card {
      background: white;
      padding: 30px;
      border-radius: 8px;
      text-align: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      transition: transform 0.3s;
    }

    .feature-card:hover {
      transform: translateY(-5px);
    }

    .feature-icon {
      font-size: 48px;
      margin-bottom: 15px;
    }

    .feature-card h3 {
      margin-bottom: 10px;
      color: #4CAF50;
    }

    .info-section {
      background: white;
      padding: 40px;
      border-radius: 8px;
      margin-bottom: 30px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .info-section h2 {
      text-align: center;
      margin-bottom: 40px;
      color: #333;
    }

    .steps {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 30px;
    }

    .step {
      text-align: center;
    }

    .step-number {
      display: inline-block;
      width: 50px;
      height: 50px;
      line-height: 50px;
      background: #4CAF50;
      color: white;
      border-radius: 50%;
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 15px;
    }

    .step h4 {
      margin-bottom: 10px;
      color: #333;
    }

    .disclaimer {
      background: #fff3cd;
      border: 1px solid #ffc107;
      padding: 20px;
      border-radius: 8px;
      text-align: center;
    }

    .disclaimer p {
      margin: 0;
      color: #856404;
    }
  `]
})
export class HomeComponent {
  constructor(private router: Router) {}

  goToPrediction() {
    this.router.navigate(['/prediction']);
  }
}

