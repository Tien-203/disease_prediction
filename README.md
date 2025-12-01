# Disease Prediction Application

A symptom-based disease prediction system with FastAPI backend and Angular frontend, deployed using Docker.

## Prerequisites

- **Docker** and **Docker Compose**

## Quick Start
```bash
docker-compose up --build -d
```

**Access the application:**
- Frontend: http://localhost:4200
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## ML Pipeline: Training the Model

You can view datasets, modify data, and retrain the model directly through the web UI. Alternatively, you can train the model using the command-line scripts below.

Run these commands from the `backend` directory:

### Step 1: Download Data
```bash
cd backend
uv run python ml/scripts/download_data.py
```

### Step 2: Preprocess Data
```bash
uv run python ml/scripts/preprocess_data_with_groups.py
```

### Step 3: Train Model
```bash
uv run python ml/scripts/train_model_with_groups.py
```

### Step 4: Evaluate Model
```bash
uv run python ml/scripts/evaluate_model.py
```

**Output:** Trained models are saved to `backend/ml/models/`

**⚠️ Gemini API Limitation:**
- The application uses Google Gemini API free tier for natural language symptom extraction
- Once the free tier quota is exceeded, natural language prediction will stop working
- Standard symptom selection will continue to work normally
- Configure `GEMINI_API_KEY` in `backend/.env` to enable this feature (optional)