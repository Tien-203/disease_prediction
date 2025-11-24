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

### Step 2: Preprocess Data with Groups

```bash
python ml/scripts/preprocess_data_with_groups.py
```

This processes the raw data by mapping symptoms to 13 groups, saving the result to `ml/data/processed/processed_dataset_with_groups.csv`.

### Step 3: Train Model with Groups

```bash
python ml/scripts/train_model_with_groups.py
```

This trains a Random Forest classifier using group-based features and saves:
- `ml/models/random_forest_model.pkl` - Trained model
- `ml/models/label_encoder.pkl` - Disease label encoder
- `ml/models/feature_names.pkl` - Group feature names (13 groups)
- `ml/models/group_encoders.pkl` - Group encoders for symptom combinations
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
│   ├── preprocess_data_with_groups.py
│   ├── train_model_with_groups.py
│   ├── evaluate_model.py
│   ├── test_model_inference.py
│   └── utils.py
└── requirements.txt
```

## Model Details

**Algorithm**: Random Forest Classifier
**Parameters**:
- n_estimators: 100
- max_depth: None
- random_state: 42

**Input**: 13 group-based features (symptoms mapped to groups)
**Output**: Predicted disease with confidence score

**Groups**: pain, respiratory, fever, digestive, urinary, skin, neurological, vision, energy, mental, joint_muscle, appetite_weight, other

## Using the Trained Model

After training, the model files in `ml/models/` will be automatically loaded by the FastAPI backend when it starts.

## Notes

- The dataset contains symptom-disease mappings
- Symptoms are mapped to 13 groups before training
- Each group contains symptom combinations (comma-separated symptom names)
- Group encoders are used to encode symptom combinations to numerical values
- The model supports multiple disease classifications
- Training typically takes 1-5 minutes depending on dataset size
