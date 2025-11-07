# Disease Prediction Frontend

Angular frontend for the Symptom-Based Disease Prediction Application.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Angular CLI: `npm install -g @angular/cli`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
# or
ng serve
```

The application will be available at http://localhost:4200

## 📁 Project Structure

```
src/
├── app/
│   ├── core/                   # Core services and interceptors
│   │   ├── services/
│   │   │   └── api.service.ts
│   │   └── interceptors/
│   │       └── http-error.interceptor.ts
│   │
│   ├── shared/                 # Shared components
│   │   └── components/
│   │       └── header.component.ts
│   │
│   ├── features/               # Feature modules
│   │   ├── home/
│   │   │   └── home.component.ts
│   │   └── prediction/
│   │       ├── components/
│   │       ├── services/
│   │       │   └── prediction.service.ts
│   │       ├── models/
│   │       │   ├── symptom.model.ts
│   │       │   ├── disease.model.ts
│   │       │   └── prediction.model.ts
│   │       ├── prediction.component.ts
│   │       ├── prediction.component.html
│   │       └── prediction.component.scss
│   │
│   ├── app.component.ts
│   ├── app.config.ts
│   └── app.routes.ts
│
├── environments/
│   ├── environment.ts          # Development config
│   └── environment.prod.ts     # Production config
│
├── assets/
└── styles.scss                 # Global styles
```

## 🎨 Features

- **Home Page**: Landing page with app introduction
- **Prediction**: Select symptoms and get disease predictions
- **Results Display**: Shows prediction with confidence score, disease info, and precautions
- **Responsive Design**: Works on desktop and mobile devices

## 🔧 Configuration

Edit `src/environments/environment.ts` to configure the API URL:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1'
};
```

## 🛠️ Development

### Run Development Server
```bash
npm start
```

### Build for Production
```bash
npm run build
```

### Run Tests
```bash
npm test
```

## 📡 API Integration

The frontend connects to the FastAPI backend through the `ApiService` and `PredictionService`.

Key endpoints used:
- `GET /symptoms` - Get available symptoms
- `POST /predict` - Submit symptoms for prediction
- `GET /health` - Check API health

## 🎯 Key Components

### HomeComponent
Landing page with app overview and navigation to prediction page.

### PredictionComponent
Main prediction interface where users:
1. Enter optional patient info (name, age)
2. Select symptoms from a searchable list
3. Submit for prediction
4. View results with confidence scores and disease information

### HeaderComponent
Navigation header with links to Home and Prediction pages.

## 📱 Usage

1. **Navigate** to http://localhost:4200
2. **Click** "Start Prediction" on the home page
3. **Select** symptoms you're experiencing
4. **Click** "Predict Disease"
5. **View** the prediction results with recommendations

## ⚠️ Notes

- Ensure the backend API is running at http://localhost:8000
- The application is for educational purposes only
- Not a substitute for professional medical advice

## 🐛 Troubleshooting

### CORS Errors
Make sure the backend is configured to allow requests from http://localhost:4200

### API Connection Issues
1. Check backend is running: http://localhost:8000/docs
2. Verify API URL in environment.ts
3. Check browser console for errors

### Build Errors
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

## 📚 Learn More

- [Angular Documentation](https://angular.io/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [RxJS Documentation](https://rxjs.dev/)

