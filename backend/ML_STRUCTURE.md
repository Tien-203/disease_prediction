# ML Directory Structure

This document explains the two ML-related directories in the backend and their purposes.

## Directory Overview

```
backend/
├── app/ml/              # ML Integration (Runtime)
└── ml/                  # ML Training (Development)
```

## 1. `/backend/app/ml/` - ML Integration Module

**Purpose**: Runtime ML integration for the FastAPI application

**Contains**:
- `model_loader.py` - Loads trained models at application startup
- `predictor.py` - Makes predictions using loaded models
- `preprocessor.py` - Preprocesses input data for predictions
- `__init__.py` - Module initialization

**Used by**: FastAPI application during runtime to serve predictions

**When to modify**: When changing how the application loads or uses models

## 2. `/backend/ml/` - ML Training Scripts

**Purpose**: Training, evaluating, and managing ML models

**Structure**:
```
ml/
├── data/
│   ├── raw/              # Raw datasets from Kaggle
│   └── processed/        # Cleaned and processed data
├── models/               # Trained model files (*.pkl)
├── notebooks/            # Jupyter notebooks for exploration
├── scripts/              # Training pipeline scripts
│   ├── download_data.py  # Download dataset from Kaggle
│   ├── preprocess_data.py # Clean and prepare data
│   ├── train_model.py    # Train the Random Forest model
│   ├── evaluate_model.py # Evaluate model performance
│   └── utils.py          # Utility functions
├── requirements.txt      # ML-specific dependencies
└── README.md             # ML training documentation
```

**Used by**: Data scientists and developers for training and improving models

**When to modify**: When training new models or updating the ML pipeline

## Workflow

### Training Phase (Development)
1. Use scripts in `/backend/ml/scripts/` to:
   - Download data
   - Preprocess data
   - Train models
   - Evaluate performance
2. Trained models are saved to `/backend/ml/models/`

### Prediction Phase (Runtime)
1. FastAPI app starts
2. Code in `/backend/app/ml/` loads models from `/backend/ml/models/`
3. API endpoints use loaded models to make predictions

## Key Points

- **`/backend/app/ml/`**: Part of the application code (runtime)
- **`/backend/ml/`**: Development/training environment (offline)
- Models trained in `/backend/ml/` are loaded by `/backend/app/ml/`
- Both directories are necessary and serve different purposes
- No ML directory exists at the root level - everything ML-related is in `/backend/`

## Training a New Model

```bash
cd backend

# Download data
python ml/scripts/download_data.py

# Preprocess
python ml/scripts/preprocess_data.py

# Train
python ml/scripts/train_model.py

# The trained model will be saved to ml/models/
# and automatically loaded by the FastAPI app on next startup
```

## Model Files Location

After training, you'll find:
- `ml/models/random_forest_model.pkl` - Trained model
- `ml/models/label_encoder.pkl` - Disease label encoder
- `ml/models/feature_names.pkl` - Feature names
- `ml/models/model_metadata.json` - Performance metrics

These files are referenced in `app/core/config.py` and loaded by `app/ml/model_loader.py`.

