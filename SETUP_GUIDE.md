# 🚀 Complete Setup Guide - Disease Prediction Application

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**
- **Node.js 18+** and npm
- **PostgreSQL 13+**
- **Angular CLI**: `npm install -g @angular/cli`
- **uv** (Python package manager)

### Install uv (if not already installed)

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 🗄️ Step 1: Setup PostgreSQL Database

### Create Database

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database and user
CREATE DATABASE disease_prediction;
CREATE USER disease_user WITH PASSWORD 'disease_password';
GRANT ALL PRIVILEGES ON DATABASE disease_prediction TO disease_user;

-- Exit
\q
```

Or using command line:
```bash
createdb disease_prediction
```

---

## 🔧 Step 2: Setup Backend

### 2.1 Install Dependencies

```bash
cd backend
uv sync
```

This will:
- Create a virtual environment
- Install all dependencies from `pyproject.toml`

### 2.2 Configure Environment

The `.env` file is already created with default values. Update if needed:

```bash
# Edit backend/.env if you changed database credentials
```

### 2.3 Initialize Database

The database tables will be created automatically when you first run the application.

---

## 🤖 Step 3: Train Machine Learning Model

This is **crucial** - the application won't work without a trained model!

```bash
# Make sure you're in the backend directory
cd backend

# Step 1: Download dataset from Kaggle (requires Kaggle API credentials)
python ml/scripts/download_data.py

# Step 2: Preprocess the data
python ml/scripts/preprocess_data.py

# Step 3: Train the Random Forest model
python ml/scripts/train_model.py

# Optional: Evaluate the model
python ml/scripts/evaluate_model.py
```

### Setting up Kaggle API

1. Create account at https://www.kaggle.com
2. Go to Account settings → API → "Create New API Token"
3. Place `kaggle.json` in:
   - Windows: `C:\Users\<Username>\.kaggle\kaggle.json`
   - Linux/Mac: `~/.kaggle/kaggle.json`
4. Set permissions (Linux/Mac): `chmod 600 ~/.kaggle/kaggle.json`

**Expected Output:**
- `ml/data/raw/` - Downloaded dataset
- `ml/data/processed/` - Cleaned data
- `ml/models/` - Trained model files (*.pkl)

---

## ▶️ Step 4: Run Backend

```bash
# From backend directory
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify Backend is Running:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/api/v1/health

---

## 🎨 Step 5: Setup Frontend

### 5.1 Install Dependencies

```bash
cd frontend
npm install
```

### 5.2 Verify Configuration

Check `src/environments/environment.ts`:
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1',  // Should match backend
  appName: 'Disease Prediction System',
  version: '1.0.0'
};
```

### 5.3 Run Frontend

```bash
npm start
# or
ng serve
```

**Access Frontend:**
- http://localhost:4200

---

## ✅ Step 6: Verify Everything Works

### 6.1 Backend Health Check

Open browser: http://localhost:8000/api/v1/health

Expected response:
```json
{
  "status": "healthy",
  "app_name": "Disease Prediction API",
  "version": "1.0.0",
  "database": "connected",
  "ml_model": "loaded"
}
```

**Important:** `ml_model` should be `"loaded"`. If it says `"not loaded"`, you need to train the model (Step 3).

### 6.2 Test API Endpoints

Go to http://localhost:8000/docs and test:

1. **GET /api/v1/symptoms** - Should return list of symptoms
2. **POST /api/v1/predict** - Test with sample data:
```json
{
  "symptoms": ["fever", "cough", "fatigue"]
}
```

### 6.3 Test Frontend

1. Open http://localhost:4200
2. Click "Start Prediction"
3. Select some symptoms
4. Click "Predict Disease"
5. View results

---

## 🎯 Quick Reference

### Start Backend
```bash
cd backend
uv run uvicorn app.main:app --reload
```

### Start Frontend
```bash
cd frontend
npm start
```

### Train New Model
```bash
cd backend
python ml/scripts/train_model.py
```

---

## 🐛 Common Issues & Solutions

### Issue: "ML model not loaded"

**Solution:** Train the model first
```bash
cd backend
python ml/scripts/download_data.py
python ml/scripts/preprocess_data.py
python ml/scripts/train_model.py
```

### Issue: CORS errors in browser

**Solution:** Check backend CORS settings in `backend/app/core/config.py`:
```python
CORS_ORIGINS: List[str] = Field(
    default=["http://localhost:4200"],
    description="Allowed CORS origins"
)
```

### Issue: Database connection error

**Solution:** 
1. Check PostgreSQL is running
2. Verify credentials in `backend/.env`
3. Ensure database exists

### Issue: "Command 'uv' not found"

**Solution:** Install uv:
```powershell
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Issue: Frontend can't connect to backend

**Solution:**
1. Verify backend is running on port 8000
2. Check `frontend/src/environments/environment.ts` has correct API URL
3. Check browser console for errors

### Issue: Kaggle dataset download fails

**Solution:**
1. Verify Kaggle API credentials are set up
2. Check internet connection
3. Try manually downloading from Kaggle and place in `backend/ml/data/raw/`

---

## 📊 Testing the Application

### Manual Test Flow

1. **Start both servers** (backend + frontend)
2. **Open** http://localhost:4200
3. **Navigate** to Prediction page
4. **Select** 3-5 symptoms
5. **Click** "Predict Disease"
6. **Verify**:
   - Prediction is returned
   - Confidence score is displayed
   - Disease information is shown
   - Alternative predictions are listed

### Test with Swagger UI

1. Open http://localhost:8000/docs
2. Test each endpoint:
   - GET /symptoms
   - GET /diseases
   - POST /predict
   - GET /health

---

## 🎓 For Your School Presentation

### Demo Checklist

- [ ] Backend running and showing "ml_model": "loaded"
- [ ] Frontend running and accessible
- [ ] Can select symptoms and get predictions
- [ ] Results display with confidence scores
- [ ] Disease information shows properly

### Talking Points

1. **Architecture**: Explain Backend → ML → Database → Frontend flow
2. **ML Model**: Random Forest with X% accuracy
3. **Tech Stack**: FastAPI, Angular, PostgreSQL, scikit-learn
4. **Features**: Real-time prediction, confidence scoring, disease info

### Screenshots to Prepare

1. Home page
2. Symptom selection page
3. Prediction results
4. API documentation (Swagger)
5. Database schema

---

## 📚 Project Structure Summary

```
disease_prediction/
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   ├── ml/                 # ML training scripts & models
│   └── tests/              # Tests
├── frontend/               # Angular frontend
│   └── src/
│       └── app/           # Angular components
├── instruction/            # Documentation
│   ├── codebase_structure.md
│   └── school_project_notes.md
└── README.md              # Main documentation
```

---

## 🎉 Success!

If you've followed all steps, you should now have:

✅ Backend API running on port 8000  
✅ ML model trained and loaded  
✅ Frontend running on port 4200  
✅ Database connected  
✅ Full prediction flow working  

**Next Steps:**
- Test the complete flow
- Prepare your demonstration
- Take screenshots for your report
- Practice your presentation

---

## 📞 Need Help?

Check these resources:
- `README.md` - Main project documentation
- `backend/README.md` - Backend-specific docs
- `backend/ml/README.md` - ML training docs
- `frontend/README.md` - Frontend-specific docs
- `instruction/school_project_notes.md` - School project tips

Good luck with your school project! 🚀

