"""Train Random Forest model for disease prediction using symptom groups"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from collections import defaultdict
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
from loguru import logger
import sys
import json


def train_disease_prediction_model_with_groups(data_file: str, models_dir: str):
    """
    Train Random Forest classifier for disease prediction using symptom groups
    
    Args:
        data_file: Path to processed dataset CSV file (with groups)
        models_dir: Directory to save trained models
    """
    logger.info("Starting model training with symptom groups...")
    
    # Load data
    logger.info(f"Loading data from {data_file}...")
    df = pd.read_csv(data_file)
    
    logger.info(f"Dataset shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    
    # Identify target column (disease/prognosis)
    target_columns = ['disease', 'prognosis', 'Disease', 'Prognosis']
    target_col = None
    
    for col in target_columns:
        if col in df.columns:
            target_col = col
            break
    
    if target_col is None:
        # Use last column as target
        target_col = df.columns[-1]
        logger.warning(f"No standard target column found, using '{target_col}' as target")
    
    logger.info(f"Target column: {target_col}")
    
    # Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Get feature names (should be the 13 groups)
    feature_names = X.columns.tolist()
    logger.info(f"Number of group features: {len(feature_names)}")
    logger.info(f"Group features: {feature_names}")
    
    # Encode categorical group features (symptom names) to numerical values
    logger.info("Encoding categorical group features...")
    group_encoders = {}
    X_encoded = X.copy()
    
    # Replace empty strings with a special value for encoding
    X_encoded = X_encoded.replace('', 'NO_SYMPTOM')
    
    # Encode each group column
    for col in feature_names:
        logger.info(f"Encoding group '{col}'...")
        encoder = LabelEncoder()
        # Fit and transform the column
        X_encoded[col] = encoder.fit_transform(X_encoded[col].astype(str))
        group_encoders[col] = encoder
        logger.info(f"  Found {len(encoder.classes_)} unique symptom combinations in group '{col}'")
    
    # Encode target labels
    logger.info("Encoding disease labels...")
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    logger.info(f"Number of unique diseases: {len(label_encoder.classes_)}")
    logger.info(f"Diseases: {label_encoder.classes_[:10]}{'...' if len(label_encoder.classes_) > 10 else ''}")
    
    # Split data
    logger.info("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )
    
    logger.info(f"Training set size: {X_train.shape[0]}")
    logger.info(f"Test set size: {X_test.shape[0]}")
    
    # Train Random Forest model
    logger.info("Training Random Forest classifier...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    
    rf_model.fit(X_train, y_train)
    logger.success("Model training completed!")
    
    # Evaluate model
    logger.info("\nEvaluating model...")
    y_train_pred = rf_model.predict(X_train)
    y_test_pred = rf_model.predict(X_test)
    
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    
    logger.info(f"Training Accuracy: {train_accuracy:.4f}")
    logger.info(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Calculate additional metrics
    precision = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)
    
    logger.info(f"Precision: {precision:.4f}")
    logger.info(f"Recall: {recall:.4f}")
    logger.info(f"F1-Score: {f1:.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    logger.info("\nGroup feature importance:")
    print(feature_importance)
    
    # Save models
    models_path = Path(models_dir)
    models_path.mkdir(parents=True, exist_ok=True)
    
    model_file = models_path / "random_forest_model.pkl"
    encoder_file = models_path / "label_encoder.pkl"
    features_file = models_path / "feature_names.pkl"
    group_encoders_file = models_path / "group_encoders.pkl"
    metadata_file = models_path / "model_metadata.json"
    
    logger.info("\nSaving models...")
    joblib.dump(rf_model, model_file)
    joblib.dump(label_encoder, encoder_file)
    joblib.dump(feature_names, features_file)
    joblib.dump(group_encoders, group_encoders_file)
    
    logger.info(f"Model saved to {model_file}")
    logger.info(f"Label encoder saved to {encoder_file}")
    logger.info(f"Feature names saved to {features_file}")
    logger.info(f"Group encoders saved to {group_encoders_file}")
    
    # Save metadata
    metadata = {
        "model_type": "RandomForestClassifier",
        "model_version": "group_based",
        "n_estimators": 100,
        "train_accuracy": float(train_accuracy),
        "test_accuracy": float(test_accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "n_features": len(feature_names),
        "n_classes": len(label_encoder.classes_),
        "classes": label_encoder.classes_.tolist(),
        "feature_names": feature_names,
        "feature_importance": feature_importance.to_dict('records')
    }
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Metadata saved to {metadata_file}")
    
    logger.success("\n✓ Model training completed successfully!")
    logger.info(f"\nModel files location: {models_path}")
    logger.info("You can now start the FastAPI backend to use the trained model.")
    logger.info("\nNote: This model uses symptom groups instead of individual symptoms.")


if __name__ == "__main__":
    # Setup logging
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # Paths
    base_dir = Path(__file__).parent.parent
    processed_data_file = base_dir / "data" / "processed" / "processed_dataset_with_groups.csv"
    models_dir = base_dir / "models"
    
    # Check if processed data exists
    if not processed_data_file.exists():
        logger.error(f"Processed data not found: {processed_data_file}")
        logger.info("Please run preprocess_data_with_groups.py first")
        sys.exit(1)
    
    # Train model
    train_disease_prediction_model_with_groups(str(processed_data_file), str(models_dir))


