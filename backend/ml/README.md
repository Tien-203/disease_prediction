# Disease Prediction - Machine Learning

This directory contains scripts and data for training the disease prediction model.

## Setup

### 1. Install Dependencies

From the backend directory:

```bash
cd backend
uv add kagglehub
```

Or install all ML requirements:
```bash
pip install -r ml/requirements.txt
```

### 2. Setup Kaggle API

To download datasets from Kaggle, you need to set up your Kaggle API credentials:

1. Create a Kaggle account at https://www.kaggle.com
2. Go to Account settings → API → "Create New API Token"
3. This downloads `kaggle.json`
4. Place it in:
   - Windows: `C:\Users\<Username>\.kaggle\kaggle.json`
   - Linux/Mac: `~/.kaggle/kaggle.json`
5. Set permissions (Linux/Mac): `chmod 600 ~/.kaggle/kaggle.json`

## Training Pipeline

Run these commands from the **backend** directory:

### Step 1: Download Dataset

```bash
python ml/scripts/download_data.py
```

This downloads a disease-symptom dataset from Kaggle and saves it to `ml/data/raw/`.

### Step 2: Preprocess Data

```bash
python ml/scripts/preprocess_data.py
```

This cleans and processes the raw data, saving the result to `ml/data/processed/`.

### Step 3: Train Model

```bash
python ml/scripts/train_model.py
```

This trains a Random Forest classifier and saves:
- `ml/models/random_forest_model.pkl` - Trained model
- `ml/models/label_encoder.pkl` - Disease label encoder
- `ml/models/feature_names.pkl` - Feature names
- `ml/models/model_metadata.json` - Model performance metrics

### Step 4: Evaluate Model

```bash
python ml/scripts/evaluate_model.py
```

This displays model performance metrics and feature importance.

## Project Structure

```
backend/ml/
├── data/
│   ├── raw/              # Raw downloaded data
│   └── processed/        # Processed data
├── models/               # Trained models
├── notebooks/            # Jupyter notebooks for exploration
├── scripts/              # Training scripts
│   ├── download_data.py
│   ├── preprocess_data.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   └── utils.py
└── requirements.txt
```

## Model Details

**Algorithm**: Random Forest Classifier
**Parameters**:
- n_estimators: 100
- max_depth: None
- random_state: 42

**Input**: Binary feature vector representing symptoms
**Output**: Predicted disease with confidence score

## Using the Trained Model

After training, the model files in `ml/models/` will be automatically loaded by the FastAPI backend when it starts.

## Notes

- The dataset contains symptom-disease mappings
- Features are binary (symptom present/absent)
- The model supports multiple disease classifications
- Training typically takes 1-5 minutes depending on dataset size
