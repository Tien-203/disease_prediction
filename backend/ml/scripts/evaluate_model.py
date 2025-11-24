"""Evaluate trained group-based model"""
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import (
    classification_report, 
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
from loguru import logger
import sys
import json


def evaluate_model(models_dir: str, data_file: str):
    """
    Evaluate trained group-based model
    
    Args:
        models_dir: Directory containing trained models
        data_file: Path to test dataset (processed_dataset_with_groups.csv)
    """
    models_path = Path(models_dir)
    
    # Load models
    logger.info("Loading models...")
    model = joblib.load(models_path / "random_forest_model.pkl")
    label_encoder = joblib.load(models_path / "label_encoder.pkl")
    feature_names = joblib.load(models_path / "feature_names.pkl")
    
    # Load group encoders (required for group-based model)
    group_encoders_path = models_path / "group_encoders.pkl"
    if group_encoders_path.exists():
        logger.info("Loading group encoders...")
        group_encoders = joblib.load(group_encoders_path)
        logger.info(f"Loaded encoders for {len(group_encoders)} groups")
    else:
        logger.error("Group encoders not found! This is required for group-based model.")
        sys.exit(1)
    
    # Load metadata
    with open(models_path / "model_metadata.json", 'r') as f:
        metadata = json.load(f)
    
    logger.info("\n" + "=" * 80)
    logger.info("Model Information")
    logger.info("=" * 80)
    logger.info(f"Model Type: {metadata.get('model_type', 'Unknown')}")
    logger.info(f"Model Version: {metadata.get('model_version', 'standard')}")
    logger.info(f"Number of Features: {metadata['n_features']}")
    logger.info(f"Number of Classes: {metadata['n_classes']}")
    logger.info(f"Test Accuracy: {metadata['test_accuracy']:.4f}")
    logger.info(f"Precision: {metadata['precision']:.4f}")
    logger.info(f"Recall: {metadata['recall']:.4f}")
    logger.info(f"F1-Score: {metadata['f1_score']:.4f}")
    
    # Display feature information
    logger.info(f"\nFeatures ({len(feature_names)}):")
    for i, feature in enumerate(feature_names, 1):
        logger.info(f"  {i}. {feature}")
    
    # Display group encoder information if available
    if group_encoders:
        logger.info(f"\nGroup Encoders Information:")
        for group_name, encoder in group_encoders.items():
            num_classes = len(encoder.classes_)
            logger.info(f"  {group_name}: {num_classes} unique symptom combinations")
            # Show sample combinations
            sample_classes = list(encoder.classes_[:5])
            if num_classes > 5:
                sample_classes.append("...")
            logger.info(f"    Samples: {', '.join(str(c) for c in sample_classes)}")
    
    # Display feature importance
    if 'feature_importance' in metadata:
        logger.info(f"\nGroup Feature Importance:")
        for i, feature_info in enumerate(metadata['feature_importance'], 1):
            logger.info(f"  {i}. {feature_info['feature']}: {feature_info['importance']:.4f}")
    elif 'top_10_features' in metadata:
        logger.info(f"\nTop 10 Important Features:")
        for i, feature in enumerate(metadata['top_10_features'][:10], 1):
            logger.info(f"  {i}. {feature['feature']}: {feature['importance']:.4f}")
    
    # Load and prepare test data
    logger.info("\n" + "=" * 80)
    logger.info("Loading Test Data")
    logger.info("=" * 80)
    logger.info(f"Loading data from {data_file}...")
    
    df = pd.read_csv(data_file)
    logger.info(f"Dataset shape: {df.shape}")
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Identify target column
    target_columns = ['disease', 'prognosis']
    target_col = None
    for col in target_columns:
        if col in df.columns:
            target_col = col
            break
    
    if target_col is None:
        target_col = df.columns[-1]
        logger.warning(f"No standard target column found, using '{target_col}' as target")
    
    # Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Encode data with group encoders
    if group_encoders:
        logger.info("\nEncoding test data with group encoders...")
        X_encoded = X.copy()
        
        # Replace empty strings with 'nan' to match training behavior
        # During training, NaN values become 'nan' string when converted to str
        X_encoded = X_encoded.replace('', 'nan')
        X_encoded = X_encoded.fillna('nan')
        
        # Encode each group column using the loaded encoders
        for col in feature_names:
            if col in group_encoders:
                encoder = group_encoders[col]
                try:
                    # Transform the column (convert to string first to handle any remaining NaN)
                    X_encoded[col] = X_encoded[col].astype(str)
                    # 'nan' string should be in encoder classes (from training)
                    X_encoded[col] = encoder.transform(X_encoded[col])
                except ValueError:
                    # Handle unseen symptom combinations
                    logger.warning(f"Some symptom combinations in group '{col}' not seen during training")
                    # Get unique values in the column
                    unique_vals = X_encoded[col].astype(str).unique()
                    seen_vals = set(encoder.classes_)
                    unseen_vals = set(unique_vals) - seen_vals
                    
                    if unseen_vals:
                        logger.debug(f"Unseen values in '{col}': {list(unseen_vals)[:5]}")
                        # Replace unseen values with 'nan' encoding if available, otherwise 0
                        def encode_with_fallback(x):
                            if x in seen_vals:
                                return encoder.transform([x])[0]
                            elif 'nan' in seen_vals:
                                # Use 'nan' encoding if available (matches training behavior)
                                return encoder.transform(['nan'])[0]
                            else:
                                return 0  # Default to 0 if 'nan' not available
                        
                        X_encoded[col] = X_encoded[col].astype(str).apply(encode_with_fallback)
            else:
                logger.warning(f"No encoder found for group '{col}', using original values")
        
        # Ensure columns are in the correct order matching feature_names
        # This is critical for model prediction
        X_test = X_encoded[feature_names]
    else:
        logger.error("Group encoders not available!")
        sys.exit(1)
    
    # Encode target labels
    logger.info("Encoding target labels...")
    y_encoded = label_encoder.transform(y)
    
    logger.info(f"Test set size: {len(X_test)}")
    logger.info(f"Number of features: {X_test.shape[1]}")
    
    # Make predictions
    logger.info("\n" + "=" * 80)
    logger.info("Running Predictions")
    logger.info("=" * 80)
    logger.info("Making predictions on test data...")
    
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_encoded, y_pred)
    precision = precision_score(y_encoded, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_encoded, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_encoded, y_pred, average='weighted', zero_division=0)
    
    logger.info("\n" + "=" * 80)
    logger.info("Evaluation Results")
    logger.info("=" * 80)
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"Precision: {precision:.4f}")
    logger.info(f"Recall: {recall:.4f}")
    logger.info(f"F1-Score: {f1:.4f}")
    
    # Classification report
    logger.info("\nDetailed Classification Report:")
    logger.info("\n" + classification_report(
        y_encoded, 
        y_pred, 
        target_names=label_encoder.classes_,
        zero_division=0
    ))
    
    # Confusion matrix (for top diseases)
    logger.info("\nConfusion Matrix (Top 10 Diseases):")
    top_diseases = label_encoder.classes_[:10]
    top_indices = [list(label_encoder.classes_).index(d) for d in top_diseases]
    
    # Filter predictions and true labels to top diseases
    mask = np.isin(y_encoded, top_indices) | np.isin(y_pred, top_indices)
    if mask.sum() > 0:
        y_encoded_top = y_encoded[mask]
        y_pred_top = y_pred[mask]
        
        # Create mapping for top diseases
        cm = confusion_matrix(y_encoded_top, y_pred_top, labels=top_indices)
        cm_df = pd.DataFrame(cm, index=top_diseases, columns=top_diseases)
        logger.info("\n" + str(cm_df))
    
    # Display all diseases
    logger.info(f"\n" + "=" * 80)
    logger.info(f"All Diseases ({len(metadata['classes'])}):")
    logger.info("=" * 80)
    for i, disease in enumerate(metadata['classes'], 1):
        logger.info(f"{i:3d}. {disease}")
    
    logger.info("\n" + "=" * 80)
    logger.success("✓ Model evaluation completed!")
    logger.info("=" * 80)


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
    models_dir = base_dir / "models"
    
    # Check if model exists
    if not (models_dir / "model_metadata.json").exists():
        logger.error("Model not found. Please run train_model_with_groups.py first")
        sys.exit(1)
    
    # Check for group-based model files
    group_encoders_path = models_dir / "group_encoders.pkl"
    if not group_encoders_path.exists():
        logger.error("Group encoders not found! This script only supports group-based models.")
        logger.info("Please run train_model_with_groups.py to train a group-based model")
        sys.exit(1)
    
    logger.info("Using group-based model")
    data_file = base_dir / "data" / "processed" / "processed_dataset_with_groups.csv"
    if not data_file.exists():
        logger.error(f"Group-based data file not found: {data_file}")
        logger.info("Please run preprocess_data_with_groups.py first")
        sys.exit(1)
    
    evaluate_model(str(models_dir), str(data_file))
