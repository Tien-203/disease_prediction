# Symptom-Based Disease Prediction Application - Codebase Structure

link figma: https://www.figma.com/design/McE5rlTznd6bfazTYUfZZS/Symptom-Based-Disease-Prediction-Application?node-id=0-1&t=9BhCc67J34tEXJrW-1

link notion: https://www.notion.so/httm-2a16645d50f38024b319f15fd3d22caa

## Project Overview
A full-stack application for disease prediction based on symptoms using Machine Learning (Random Forest classifier).

**Note**: This is a simplified structure for a school project. Focus on core functionality, not extensive testing or production deployment.

**Tech Stack:**
- Backend: Python 3.11+, FastAPI
- Frontend: Angular 17+
- Database: PostgreSQL
- ML: scikit-learn (Random Forest)
- Dataset: Kaggle (via kagglehub)

---

## 🎓 Project Scope

This is a **school project** focusing on demonstrating:
1. Full-stack development skills
2. Machine Learning integration
3. REST API design
4. Modern web application architecture

---

## ✅ What to Focus On

### Backend (FastAPI)
- ✅ Basic CRUD operations for symptoms and diseases
- ✅ ML model integration for predictions
- ✅ Database models and migrations
- ✅ API endpoints with proper responses
- ❌ No need for extensive unit tests
- ❌ No need for authentication/authorization
- ❌ No need for advanced security features

### Frontend (Angular)
- ✅ Clean, functional UI
- ✅ Forms for symptom selection
- ✅ Display prediction results
- ✅ Basic routing and navigation
- ❌ No need for state management (NgRx)
- ❌ No need for extensive animations
- ❌ No need for responsive design optimization

### Machine Learning
- ✅ Download and preprocess dataset
- ✅ Train Random Forest model
- ✅ Basic evaluation metrics
- ❌ No need for hyperparameter tuning
- ❌ No need for multiple model comparison
- ❌ No need for advanced feature engineering

### Database
- ✅ Basic PostgreSQL setup
- ✅ Simple tables for symptoms, diseases, predictions
- ❌ No need for complex relationships
- ❌ No need for database optimization
- ❌ No need for migrations in production

---

## Root Directory Structure

```
disease_prediction/
├── backend/                    # FastAPI backend application
├── frontend/                   # Angular frontend application
├── ml/                        # Machine learning models and training scripts
├── shared/                    # Shared configurations and utilities
├── instruction/               # Project documentation
├── .gitignore
├── README.md
└── docker-compose.yml         # Docker orchestration (optional)
```

---

## Backend Structure (`backend/`)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                           # FastAPI application entry point
│   ├── config.py                         # Configuration management (env vars, settings)
│   │
│   ├── api/                              # API routes
│   │   ├── __init__.py
│   │   ├── deps.py                       # Dependencies (DB session, auth, etc.)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── prediction.py         # Disease prediction endpoints
│   │       │   ├── symptoms.py           # Symptom management endpoints
│   │       │   ├── diseases.py           # Disease information endpoints
│   │       │   └── health.py             # Health check endpoints
│   │       └── router.py                 # API v1 router aggregation
│   │
│   ├── core/                             # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py                     # Core configuration
│   │   ├── security.py                   # Security utilities (if needed)
│   │   └── logging.py                    # Logging configuration (loguru)
│   │
│   ├── db/                               # Database
│   │   ├── __init__.py
│   │   ├── base.py                       # SQLAlchemy base
│   │   ├── session.py                    # Database session management
│   │   └── init_db.py                    # Database initialization
│   │
│   ├── models/                           # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── symptom.py                    # Symptom model
│   │   ├── disease.py                    # Disease model
│   │   ├── prediction.py                 # Prediction history model
│   │   └── user.py                       # User model (if needed)
│   │
│   ├── schemas/                          # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── symptom.py                    # Symptom schemas
│   │   ├── disease.py                    # Disease schemas
│   │   ├── prediction.py                 # Prediction schemas
│   │   └── common.py                     # Common schemas (pagination, etc.)
│   │
│   ├── services/                         # Business logic
│   │   ├── __init__.py
│   │   ├── prediction_service.py         # ML prediction service
│   │   ├── symptom_service.py            # Symptom management service
│   │   └── disease_service.py            # Disease information service
│   │
│   └── ml/                               # ML model integration
│       ├── __init__.py
│       ├── model_loader.py               # Load trained ML model
│       ├── preprocessor.py               # Data preprocessing
│       └── predictor.py                  # Prediction logic
│
├── tests/                                # Backend tests (optional for school project)
│   └── __init__.py
│
├── alembic/                              # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── pyproject.toml                        # Python project configuration (uv)
├── requirements.txt                      # Python dependencies (generated)
├── .env.example                          # Environment variables example
├── .env                                  # Environment variables (gitignored)
└── README.md                             # Backend documentation
```

---

## ML Structure (`ml/`)

```
ml/
├── data/                                 # Data storage
│   ├── raw/                              # Raw downloaded data
│   ├── processed/                        # Processed/cleaned data
│   └── .gitkeep
│
├── models/                               # Trained models
│   ├── random_forest_model.pkl          # Trained Random Forest model
│   ├── label_encoder.pkl                # Label encoder for diseases
│   ├── feature_names.pkl                # Feature names for consistency
│   └── model_metadata.json              # Model metrics and metadata
│
├── notebooks/                            # Jupyter notebooks for exploration
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_model_evaluation.ipynb
│
├── scripts/                              # Training and evaluation scripts
│   ├── __init__.py
│   ├── download_data.py                  # Download dataset from Kaggle via kagglehub
│   ├── preprocess_data.py                # Data preprocessing
│   ├── train_model.py                    # Train Random Forest model
│   ├── evaluate_model.py                 # Evaluate model performance
│   └── utils.py                          # Utility functions
│
├── requirements.txt                      # ML dependencies
└── README.md                             # ML documentation
```

---

## Frontend Structure (`frontend/`)

```
frontend/
├── src/
│   ├── app/
│   │   ├── core/                         # Core module (singleton services)
│   │   │   ├── services/
│   │   │   │   ├── api.service.ts        # HTTP client wrapper
│   │   │   │   ├── error-handler.service.ts
│   │   │   │   └── logger.service.ts
│   │   │   ├── interceptors/
│   │   │   │   ├── http-error.interceptor.ts
│   │   │   │   └── loading.interceptor.ts
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts         # If authentication needed
│   │   │   └── core.module.ts
│   │   │
│   │   ├── shared/                       # Shared module (reusable components)
│   │   │   ├── components/
│   │   │   │   ├── header/
│   │   │   │   │   ├── header.component.ts
│   │   │   │   │   ├── header.component.html
│   │   │   │   │   └── header.component.scss
│   │   │   │   ├── footer/
│   │   │   │   ├── loading-spinner/
│   │   │   │   └── symptom-selector/    # Reusable symptom selector
│   │   │   ├── directives/
│   │   │   ├── pipes/
│   │   │   └── shared.module.ts
│   │   │
│   │   ├── features/                     # Feature modules
│   │   │   ├── home/
│   │   │   │   ├── home.component.ts
│   │   │   │   ├── home.component.html
│   │   │   │   ├── home.component.scss
│   │   │   │   └── home.routes.ts
│   │   │   │
│   │   │   ├── prediction/
│   │   │   │   ├── components/
│   │   │   │   │   ├── symptom-input/
│   │   │   │   │   ├── prediction-result/
│   │   │   │   │   └── disease-details/
│   │   │   │   ├── services/
│   │   │   │   │   └── prediction.service.ts
│   │   │   │   ├── models/
│   │   │   │   │   ├── symptom.model.ts
│   │   │   │   │   ├── disease.model.ts
│   │   │   │   │   └── prediction.model.ts
│   │   │   │   ├── prediction.component.ts
│   │   │   │   ├── prediction.component.html
│   │   │   │   ├── prediction.component.scss
│   │   │   │   └── prediction.routes.ts
│   │   │   │
│   │   │   ├── history/                  # Prediction history (optional)
│   │   │   │   ├── history.component.ts
│   │   │   │   ├── history.component.html
│   │   │   │   ├── history.component.scss
│   │   │   │   └── history.routes.ts
│   │   │   │
│   │   │   └── about/
│   │   │       ├── about.component.ts
│   │   │       ├── about.component.html
│   │   │       ├── about.component.scss
│   │   │       └── about.routes.ts
│   │   │
│   │   ├── app.component.ts              # Root component
│   │   ├── app.component.html
│   │   ├── app.component.scss
│   │   ├── app.config.ts                 # App configuration
│   │   └── app.routes.ts                 # Main routing
│   │
│   ├── assets/                           # Static assets
│   │   ├── images/
│   │   ├── icons/
│   │   └── styles/
│   │       └── themes/
│   │
│   ├── environments/                     # Environment configurations
│   │   ├── environment.ts                # Development
│   │   └── environment.prod.ts           # Production
│   │
│   ├── index.html
│   ├── main.ts
│   └── styles.scss                       # Global styles
│
├── angular.json                          # Angular configuration
├── tsconfig.json                         # TypeScript configuration
├── tsconfig.app.json
├── package.json                          # NPM dependencies
└── README.md                             # Frontend documentation
```

---

## Database Schema

### Tables

#### 1. **symptoms**
```sql
id: SERIAL PRIMARY KEY
name: VARCHAR(100) UNIQUE NOT NULL
description: TEXT
created_at: TIMESTAMP DEFAULT NOW()
updated_at: TIMESTAMP DEFAULT NOW()
```

#### 2. **diseases**
```sql
id: SERIAL PRIMARY KEY
name: VARCHAR(100) UNIQUE NOT NULL
description: TEXT
severity: VARCHAR(20)  -- mild, moderate, severe
precautions: TEXT[]
recommendations: TEXT
created_at: TIMESTAMP DEFAULT NOW()
updated_at: TIMESTAMP DEFAULT NOW()
```

#### 3. **disease_symptoms** (Many-to-Many relationship)
```sql
id: SERIAL PRIMARY KEY
disease_id: INTEGER REFERENCES diseases(id)
symptom_id: INTEGER REFERENCES symptoms(id)
weight: FLOAT  -- importance of symptom for disease
created_at: TIMESTAMP DEFAULT NOW()
```

#### 4. **predictions** (Prediction history)
```sql
id: SERIAL PRIMARY KEY
symptoms: TEXT[]  -- Array of symptom names
predicted_disease: VARCHAR(100)
confidence: FLOAT
timestamp: TIMESTAMP DEFAULT NOW()
session_id: VARCHAR(100)  -- For tracking user sessions
```

---

## API Endpoints

### Base URL: `/api/v1`

#### Health Check
- `GET /health` - Health check endpoint

#### Symptoms
- `GET /symptoms` - Get all symptoms
- `GET /symptoms/{id}` - Get symptom by ID
- `POST /symptoms` - Create new symptom (admin)
- `PUT /symptoms/{id}` - Update symptom (admin)
- `DELETE /symptoms/{id}` - Delete symptom (admin)

#### Diseases
- `GET /diseases` - Get all diseases
- `GET /diseases/{id}` - Get disease by ID
- `GET /diseases/search?name=...` - Search diseases by name
- `POST /diseases` - Create new disease (admin)
- `PUT /diseases/{id}` - Update disease (admin)
- `DELETE /diseases/{id}` - Delete disease (admin)

#### Prediction
- `POST /predict` - Predict disease based on symptoms
  - Request body: `{"symptoms": ["symptom1", "symptom2", ...]}`
  - Response: `{"disease": "...", "confidence": 0.95, "alternatives": [...]}`
- `GET /predictions/history` - Get prediction history (optional)
- `GET /predictions/{id}` - Get specific prediction

---

## Environment Variables

### Backend (.env)
```
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/disease_prediction
POSTGRES_USER=disease_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=disease_prediction

# Application
APP_NAME=Disease Prediction API
APP_VERSION=1.0.0
DEBUG=True
API_V1_PREFIX=/api/v1

# ML Model
MODEL_PATH=../ml/models/random_forest_model.pkl
LABEL_ENCODER_PATH=../ml/models/label_encoder.pkl
FEATURE_NAMES_PATH=../ml/models/feature_names.pkl

# CORS
CORS_ORIGINS=["http://localhost:4200"]

# Logging
LOG_LEVEL=INFO
```

### Frontend (environment.ts)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1',
  appName: 'Disease Prediction',
  version: '1.0.0'
};
```

---

## Key Dependencies

### Backend (pyproject.toml / requirements.txt)
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
alembic>=1.12.0
pydantic>=2.4.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
loguru>=0.7.0
scikit-learn>=1.3.0
pandas>=2.1.0
numpy>=1.24.0
joblib>=1.3.0
kagglehub>=0.2.0
python-multipart>=0.0.6
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "@angular/animations": "^17.0.0",
    "@angular/common": "^17.0.0",
    "@angular/compiler": "^17.0.0",
    "@angular/core": "^17.0.0",
    "@angular/forms": "^17.0.0",
    "@angular/platform-browser": "^17.0.0",
    "@angular/platform-browser-dynamic": "^17.0.0",
    "@angular/router": "^17.0.0",
    "rxjs": "^7.8.0",
    "tslib": "^2.6.0",
    "zone.js": "^0.14.0"
  }
}
```

### ML (ml/requirements.txt)
```
scikit-learn>=1.3.0
pandas>=2.1.0
numpy>=1.24.0
matplotlib>=3.8.0
seaborn>=0.13.0
jupyter>=1.0.0
kagglehub>=0.2.0
joblib>=1.3.0
```

---

## Coding Standards (Simplified for School Project)

### Python
- Follow PEP 8 style guide (basic formatting)
- Use type hints for main functions
- Add docstrings for important functions
- Use loguru for logging
- Comment code in English

### TypeScript/Angular
- Follow Angular style guide (basic)
- Use TypeScript properly
- Add comments for complex logic
- Keep components simple and readable

### General
- Write clear commit messages
- Keep code DRY (Don't Repeat Yourself)
- Use environment variables for configuration
- Never commit sensitive data (passwords, API keys)
- Comment complex logic in English
- **Focus on working functionality over extensive testing**

---

## 🚀 Quick Start Guide

### 1. Backend Setup (5-10 minutes)
```bash
cd backend
uv sync
python ml/scripts/download_data.py
python ml/scripts/preprocess_data.py
python ml/scripts/train_model.py
uv run uvicorn app.main:app --reload
```

### 2. Frontend Setup (5 minutes)
```bash
cd frontend
npm install
ng serve
```

### 3. Test (5 minutes)
- Open http://localhost:8000/docs - Test API
- Open http://localhost:4200 - Test UI
- Make a prediction through the UI

---

## Development Workflow (Simplified)

1. **Backend Setup**
   - Set up database and models
   - Implement API endpoints
   - Train ML model
   - Test basic functionality manually

2. **Frontend Development**
   - Set up Angular project
   - Create components and services
   - Connect to backend API
   - Implement basic UI

3. **Integration & Demo**
   - Test main user flows
   - Fix critical bugs
   - Prepare for demonstration

---

## ML Training Pipeline

1. **Download Data**: Use kagglehub to download disease-symptom dataset
2. **Preprocess**: Clean data, handle missing values, encode features
3. **Train**: Train Random Forest classifier with hyperparameter tuning
4. **Evaluate**: Calculate accuracy, precision, recall, F1-score
5. **Save**: Serialize model, encoders, and feature names
6. **Deploy**: Load model in FastAPI service for predictions

---

## 📝 Testing Strategy (Simplified)

### Manual Testing Only
- Test each API endpoint using Swagger UI (`/docs`)
- Test frontend manually in browser
- Verify prediction flow end-to-end
- No automated tests required

### What to Verify
1. ✅ ML model trains successfully
2. ✅ API endpoints return correct data
3. ✅ Frontend displays data properly
4. ✅ Prediction flow works from UI to API to ML
5. ✅ Database stores predictions

---

## 📊 Demonstration Checklist

For your school presentation, demonstrate:

1. **System Architecture** (2 min)
   - Show the project structure
   - Explain Backend → ML → Database → Frontend flow

2. **Machine Learning** (3 min)
   - Show training scripts
   - Explain Random Forest algorithm
   - Show model accuracy metrics

3. **Backend API** (2 min)
   - Show Swagger documentation
   - Test a prediction endpoint
   - Show response with confidence scores

4. **Frontend UI** (3 min)
   - Navigate through the application
   - Select symptoms
   - Show prediction results
   - Show disease information

5. **Database** (1 min)
   - Show stored predictions (optional)

---

## ⚠️ Common Issues & Solutions

### Issue: Model not loaded
**Solution**: Run the training scripts first before starting the API

### Issue: Database connection error
**Solution**: Ensure PostgreSQL is running and credentials in .env are correct

### Issue: CORS errors
**Solution**: Check that CORS_ORIGINS in backend includes http://localhost:4200

### Issue: ML dependencies error
**Solution**: Install ML requirements: `pip install -r backend/ml/requirements.txt`

---

## 📚 What to Include in Your Report

### Technical Documentation
1. System architecture diagram
2. API endpoints list
3. Database schema
4. ML model details (algorithm, accuracy, features)
5. Screenshots of the application

### Code Highlights
- API endpoint implementation
- ML model integration
- Database models
- Key frontend components

### Results
- Model accuracy metrics
- Sample predictions with confidence scores
- Application screenshots

---

## 🎯 Grading Focus Areas

Based on typical school project criteria:

1. **Functionality** (40%)
   - Does it work?
   - Can you make predictions?
   - Is the UI usable?

2. **Code Quality** (30%)
   - Is code organized and readable?
   - Are there comments?
   - Is it maintainable?

3. **ML Integration** (20%)
   - Is ML properly integrated?
   - Does the model work?
   - Are results meaningful?

4. **Documentation** (10%)
   - Is there a README?
   - Can someone else run it?
   - Is the code documented?

---

## 💡 Tips for Success

1. **Start Simple**: Get the basic flow working first
2. **Test Frequently**: Test after each major change
3. **Document as You Go**: Add comments while coding
4. **Keep It Working**: Don't break working code for fancy features
5. **Focus on Demo**: Ensure demo scenarios work perfectly
6. **Have Backup**: Take screenshots in case of demo issues

---

## 🚫 What NOT to Spend Time On

- Extensive unit tests
- Production deployment
- Advanced security features
- Performance optimization
- Responsive design for mobile
- Advanced animations
- User authentication
- Multiple user roles
- Complex state management

---

## ✨ Optional Enhancements (If You Have Time)

Priority order:
1. Better UI styling (Bootstrap/Material)
2. Prediction history display
3. Search functionality for symptoms
4. Better error messages
5. Loading indicators

---

## Deployment Considerations (Optional for School Project)

- Run locally for development and demonstration
- PostgreSQL installed locally
- Environment variables in .env file
- CORS configured for localhost
- Basic error handling and logging
- **No need for Docker/production deployment for school project**

---

## Security Best Practices

- Use environment variables for sensitive data
- Implement input validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Rate limiting for API endpoints (optional)
- HTTPS in production

---

**Remember**: The goal is to demonstrate understanding of full-stack development with ML integration, not to build a production-ready application. Focus on making it work well for your demo! 🎓

This structure ensures a clean, maintainable, scalable, and professional codebase following industry best practices.
