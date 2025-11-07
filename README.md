# Symptom-Based Disease Prediction Application

A full-stack web application for predicting diseases based on symptoms using Machine Learning.

## 🎯 Overview

This application uses a Random Forest machine learning model to predict diseases based on user-provided symptoms. It features a modern Angular frontend, FastAPI backend, and PostgreSQL database.

## 📋 Features

- **Disease Prediction**: Predict diseases based on selected symptoms
- **Confidence Scoring**: Get prediction confidence levels and alternative diagnoses
- **Disease Information**: View detailed information about predicted diseases including:
  - Description
  - Severity level
  - Precautions
  - Medical recommendations
- **Prediction History**: Track past predictions
- **Symptom Management**: Browse available symptoms
- **RESTful API**: Well-documented API endpoints

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **ML**: scikit-learn (Random Forest)
- **Logging**: Loguru
- **Package Manager**: uv

### Frontend
- **Framework**: Angular 17+
- **Language**: TypeScript
- **Styling**: SCSS

### Machine Learning
- **Algorithm**: Random Forest Classifier
- **Dataset**: Kaggle disease-symptom dataset
- **Library**: scikit-learn

## 📁 Project Structure

```
disease_prediction/
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core configuration
│   │   ├── db/               # Database setup
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── ml/               # ML integration
│   ├── ml/                   # ML training scripts
│   │   ├── data/             # Dataset storage
│   │   ├── models/           # Trained models
│   │   └── scripts/          # Training scripts
│   └── tests/                # Backend tests
│
├── frontend/                  # Angular frontend
│   └── src/
│       └── app/
│           ├── core/         # Core services
│           ├── shared/       # Shared components
│           └── features/     # Feature modules
│
└── instruction/              # Project documentation
    └── codebase_structure.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL 13+
- uv (Python package manager)
- Angular CLI

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd disease_prediction
```

#### 2. Backend Setup

```bash
cd backend

# Install uv if not already installed (Windows)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install dependencies
uv sync

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Create PostgreSQL database
createdb disease_prediction
```

#### 3. Train the ML Model

```bash
# From the backend directory
python ml/scripts/download_data.py
python ml/scripts/preprocess_data.py
python ml/scripts/train_model.py
```

#### 4. Run Backend

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- Main: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
ng serve
```

The frontend will be available at http://localhost:4200

## 📖 API Documentation

### Base URL: `http://localhost:8000/api/v1`

### Endpoints

#### Health Check
- `GET /health` - Check API health status

#### Symptoms
- `GET /symptoms` - Get all symptoms
- `GET /symptoms/{id}` - Get symptom by ID
- `POST /symptoms` - Create symptom (admin)
- `PUT /symptoms/{id}` - Update symptom (admin)
- `DELETE /symptoms/{id}` - Delete symptom (admin)

#### Diseases
- `GET /diseases` - Get all diseases
- `GET /diseases/{id}` - Get disease by ID
- `GET /diseases/search?name=flu` - Search diseases
- `POST /diseases` - Create disease (admin)
- `PUT /diseases/{id}` - Update disease (admin)
- `DELETE /diseases/{id}` - Delete disease (admin)

#### Predictions
- `POST /predict` - Predict disease from symptoms
- `GET /predict/history` - Get prediction history
- `GET /predict/{id}` - Get prediction by ID

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["fever", "cough", "fatigue"],
    "session_id": "optional-session-id"
  }'
```

### Example Response

```json
{
  "predicted_disease": "Influenza",
  "confidence": 0.95,
  "alternatives": [
    {
      "disease": "Common Cold",
      "confidence": 0.73
    }
  ],
  "symptoms_used": ["fever", "cough", "fatigue"],
  "disease_info": {
    "description": "A contagious respiratory illness",
    "severity": "moderate",
    "precautions": ["Get vaccinated", "Rest", "Stay hydrated"],
    "recommendations": "Seek medical attention if symptoms worsen"
  }
}
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
uv run pytest
```

### Frontend Tests

```bash
cd frontend
ng test
```

## 📊 Model Training

The ML model training pipeline consists of:

1. **Data Download**: Download dataset from Kaggle using kagglehub
2. **Preprocessing**: Clean and prepare data
3. **Training**: Train Random Forest classifier
4. **Evaluation**: Evaluate model performance

See `backend/ml/README.md` for detailed instructions.

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql://disease_user:password@localhost:5432/disease_prediction
APP_NAME=Disease Prediction API
API_V1_PREFIX=/api/v1
MODEL_PATH=ml/models/random_forest_model.pkl
CORS_ORIGINS=["http://localhost:4200"]
```

### Frontend Environment

Edit `frontend/src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1'
};
```

## 🎨 Design

The UI/UX design is available on Figma:
- [Figma Design](https://www.figma.com/design/McE5rlTznd6bfazTYUfZZS/Symptom-Based-Disease-Prediction-Application)

## 📚 Documentation

- [Codebase Structure](instruction/codebase_structure.md) - Detailed architecture documentation
- [Backend README](backend/README.md) - Backend-specific documentation
- [ML README](backend/ml/README.md) - ML training documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This application is for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with any questions you may have regarding a medical condition.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Dataset from Kaggle
- FastAPI framework
- Angular framework
- scikit-learn library
