"""Standalone script to test ML model inference with test cases from dataset"""
import sys
import pandas as pd
import random
from pathlib import Path
from typing import List, Tuple, Optional

# Add backend to path when run as script
if __name__ == "__main__":
    backend_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(backend_dir))

from loguru import logger
from app.ml.model_loader import ModelLoader
from app.ml.predictor import DiseasePredictor


def load_test_cases_from_dataset(dataset_path: Path, num_cases: int = 5) -> List[Tuple[str, List[str]]]:
    """
    Load test cases from raw dataset
    
    Args:
        dataset_path: Path to raw dataset CSV file
        num_cases: Number of test cases to load
        
    Returns:
        List of tuples: (actual_disease, list_of_symptoms)
    """
    logger.info(f"Loading {num_cases} test cases from dataset: {dataset_path}")
    
    # Read dataset
    df = pd.read_csv(dataset_path)
    
    # Get disease column (first column)
    disease_col = df.columns[0]
    
    # Get symptom columns (all except first)
    symptom_cols = [col for col in df.columns if col != disease_col]
    
    test_cases = []
    
    # Select diverse test cases (different diseases)
    selected_indices = []
    seen_diseases = set()
    
    for idx, row in df.iterrows():
        if len(selected_indices) >= num_cases:
            break
        
        disease = str(row[disease_col]).strip()
        
        # Collect symptoms from this row
        # IMPORTANT: Pass original symptom names (not normalized) to preprocessor
        # The preprocessor will normalize them the same way as during training
        symptoms = []
        for col in symptom_cols:
            symptom_val = str(row[col]).strip() if pd.notna(row[col]) else ''
            if symptom_val and symptom_val != '0' and symptom_val.lower() != 'nan' and symptom_val:
                # Keep original symptom name - preprocessor will normalize it
                symptoms.append(symptom_val)
        
        # Only add if we have symptoms and haven't seen this disease yet (or need more cases)
        if symptoms and (disease not in seen_diseases or len(selected_indices) < num_cases):
            test_cases.append((disease, symptoms))
            selected_indices.append(idx)
            seen_diseases.add(disease)
    
    logger.info(f"Loaded {len(test_cases)} test cases from dataset")
    return test_cases


def generate_random_test_cases(dataset_path: Path, num_cases: int = 5, min_symptoms: int = 3, max_symptoms: int = 7) -> List[Tuple[Optional[str], List[str]]]:
    """
    Generate random test cases by randomly selecting symptoms from the dataset
    
    Args:
        dataset_path: Path to raw dataset CSV file
        num_cases: Number of random test cases to generate
        min_symptoms: Minimum number of symptoms per case
        max_symptoms: Maximum number of symptoms per case
        
    Returns:
        List of tuples: (None, list_of_symptoms) - None because we don't know the actual disease
    """
    logger.info(f"Generating {num_cases} random test cases from dataset: {dataset_path}")
    
    # Read dataset
    df = pd.read_csv(dataset_path)
    
    # Get disease column (first column)
    disease_col = df.columns[0]
    
    # Get symptom columns (all except first)
    symptom_cols = [col for col in df.columns if col != disease_col]
    
    # Collect all unique symptoms from the dataset
    all_symptoms = set()
    for _, row in df.iterrows():
        for col in symptom_cols:
            symptom_val = str(row[col]).strip() if pd.notna(row[col]) else ''
            if symptom_val and symptom_val != '0' and symptom_val.lower() != 'nan' and symptom_val:
                all_symptoms.add(symptom_val)
    
    all_symptoms_list = list(all_symptoms)
    logger.info(f"Found {len(all_symptoms_list)} unique symptoms in dataset")
    
    if len(all_symptoms_list) < min_symptoms:
        logger.warning(f"Not enough unique symptoms ({len(all_symptoms_list)}) to generate test cases")
        return []
    
    # Generate random test cases
    random_cases = []
    for i in range(num_cases):
        # Randomly select number of symptoms for this case
        num_symptoms = random.randint(min_symptoms, min(max_symptoms, len(all_symptoms_list)))
        
        # Randomly select symptoms
        selected_symptoms = random.sample(all_symptoms_list, num_symptoms)
        
        # Add case with None as disease (unknown for random cases)
        random_cases.append((None, selected_symptoms))
    
    logger.info(f"Generated {len(random_cases)} random test cases")
    return random_cases


def test_model_inference():
    """Test ML model inference with dummy data"""
    
    # Setup logging
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    logger.info("=" * 80)
    logger.info("ML Model Inference Test Script")
    logger.info("=" * 80)
    
    # Initialize model loader
    model_loader = ModelLoader()
    
    # Get backend directory (same as used for sys.path)
    backend_dir = Path(__file__).parent.parent.parent
    
    # Model paths (relative to backend directory)
    model_path = backend_dir / "ml" / "models" / "random_forest_model.pkl"
    label_encoder_path = backend_dir / "ml" / "models" / "label_encoder.pkl"
    feature_names_path = backend_dir / "ml" / "models" / "feature_names.pkl"
    group_encoders_path = backend_dir / "ml" / "models" / "group_encoders.pkl"
    
    # Check if group encoders exist (required for group-based models)
    logger.debug(f"Looking for group encoders at: {group_encoders_path}")
    logger.debug(f"Backend directory: {backend_dir}")
    logger.debug(f"File exists: {group_encoders_path.exists()}")
    
    if not group_encoders_path.exists():
        logger.error(f"Group encoders not found at: {group_encoders_path}")
        logger.error("This script only supports group-based models.")
        logger.info("Please run train_model_with_groups.py to train a group-based model")
        sys.exit(1)
    
    group_encoders_path_param = "ml/models/group_encoders.pkl"
    logger.info("Group-based model detected (group_encoders.pkl found)")
    
    # Load models
    logger.info("\nLoading ML models...")
    success = model_loader.load_models(
        model_path="ml/models/random_forest_model.pkl",
        label_encoder_path="ml/models/label_encoder.pkl",
        feature_names_path="ml/models/feature_names.pkl",
        group_encoders_path=group_encoders_path_param
    )
    
    if not success:
        logger.error("Failed to load models. Please ensure models are trained first.")
        logger.info("Run: python ml/scripts/train_model_with_groups.py")
        return
    
    logger.success("✓ Models loaded successfully")
    
    # Initialize predictor
    predictor = DiseasePredictor(model_loader)
    
    # Get model info
    feature_names = model_loader.get_feature_names()
    logger.info(f"\nModel Information:")
    logger.info(f"  - Number of features: {len(feature_names)}")
    logger.info(f"  - Feature names: {feature_names}")
    
    label_encoder = model_loader.get_label_encoder()
    logger.info(f"  - Number of diseases: {len(label_encoder.classes_)}")
    logger.info(f"  - Sample diseases: {list(label_encoder.classes_[:5])}")
    
    # Load test cases from dataset
    dataset_path = backend_dir / "ml" / "data" / "raw" / "dataset.csv"
    if not dataset_path.exists():
        logger.error(f"Dataset not found at: {dataset_path}")
        logger.info("Please ensure the dataset file exists")
        sys.exit(1)
    
    # Load 5 test cases from dataset (with known diseases)
    dataset_cases = load_test_cases_from_dataset(dataset_path, num_cases=5)
    
    # Generate 5 random test cases (without known diseases)
    random_cases = generate_random_test_cases(dataset_path, num_cases=5, min_symptoms=3, max_symptoms=7)
    
    # Combine test cases: first 5 from dataset, then 5 random
    test_cases = dataset_cases + random_cases
    
    logger.info("\n" + "=" * 80)
    logger.info("Running Inference Tests")
    logger.info(f"  - {len(dataset_cases)} cases from dataset (with known diseases)")
    logger.info(f"  - {len(random_cases)} random cases (unknown diseases)")
    logger.info("=" * 80)
    
    # Track results for comparison
    correct_predictions = 0
    dataset_predictions = 0  # Count only dataset cases for accuracy calculation
    total_predictions = len(test_cases)
    results_summary = []
    
    # Run inference for each test case
    for i, (actual_disease, symptoms) in enumerate(test_cases, 1):
        logger.info(f"\n{'─' * 80}")
        logger.info(f"Test Case {i}:")
        
        # Determine case type
        is_from_dataset = actual_disease is not None
        case_type = "Dataset" if is_from_dataset else "Random"
        logger.info(f"  Type: {case_type}")
        
        if is_from_dataset:
            logger.info(f"  Actual Disease: {actual_disease}")
        else:
            logger.info(f"  Actual Disease: Unknown (random case)")
        
        logger.info(f"  Input Symptoms ({len(symptoms)}): {', '.join(symptoms[:10])}{'...' if len(symptoms) > 10 else ''}")
        
        try:
            # Make prediction
            predicted_disease, confidence, alternatives = predictor.predict(symptoms)
            
            # Check if prediction is correct (only for dataset cases)
            is_correct = None
            if is_from_dataset:
                dataset_predictions += 1
                is_correct = predicted_disease.strip().lower() == actual_disease.strip().lower()
                if is_correct:
                    correct_predictions += 1
            
            # Display results
            if is_correct is not None:
                status_icon = "✓" if is_correct else "✗"
                logger.info(f"\n  Results:")
                logger.info(f"    {status_icon} Predicted Disease: {predicted_disease}")
                logger.info(f"    {'✓' if is_correct else '✗'} Actual Disease: {actual_disease}")
            else:
                logger.info(f"\n  Results:")
                logger.info(f"    Predicted Disease: {predicted_disease}")
                logger.info(f"    Actual Disease: Unknown (random case)")
            
            logger.info(f"    Confidence: {confidence:.2%}")
            
            if alternatives:
                logger.info(f"    Alternative Predictions:")
                for alt_disease, alt_confidence in alternatives[:3]:  # Show top 3
                    logger.info(f"      - {alt_disease}: {alt_confidence:.2%}")
            
            # Store result for summary
            results_summary.append({
                'case': i,
                'type': case_type,
                'actual': actual_disease if actual_disease else "Unknown",
                'predicted': predicted_disease,
                'correct': is_correct,
                'confidence': confidence
            })
            
            # Get matched/unmatched symptoms
            matched, unmatched = predictor.get_matched_symptoms(symptoms)
            if matched:
                logger.info(f"    Matched Symptoms ({len(matched)}): {', '.join(matched[:5])}{'...' if len(matched) > 5 else ''}")
            if unmatched:
                logger.warning(f"    Unmatched Symptoms ({len(unmatched)}): {', '.join(unmatched)}")
            
            # Log feature vector for debugging
            logger.debug(f"    Feature vector created (check logs above for encoding details)")
            
        except Exception as e:
            logger.error(f"  Error during prediction: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            results_summary.append({
                'case': i,
                'actual': actual_disease,
                'predicted': 'ERROR',
                'correct': False,
                'confidence': 0.0
            })
    
    # Display summary
    logger.info("\n" + "=" * 80)
    logger.info("Test Results Summary")
    logger.info("=" * 80)
    logger.info(f"Total Test Cases: {total_predictions}")
    logger.info(f"  - Dataset Cases: {len(dataset_cases)}")
    logger.info(f"  - Random Cases: {len(random_cases)}")
    
    if dataset_predictions > 0:
        logger.info(f"\nDataset Cases Results:")
        logger.info(f"  Correct Predictions: {correct_predictions}")
        logger.info(f"  Incorrect Predictions: {dataset_predictions - correct_predictions}")
        accuracy = (correct_predictions / dataset_predictions) * 100 if dataset_predictions > 0 else 0
        logger.info(f"  Accuracy: {accuracy:.2f}%")
    
    logger.info("\nDetailed Results:")
    for result in results_summary:
        if result['correct'] is not None:
            # Dataset case with known disease
            status = "✓ CORRECT" if result['correct'] else "✗ WRONG"
            logger.info(f"  Case {result['case']:2d} [{result['type']:6s}]: {status} | Actual: {result['actual']:30s} | Predicted: {result['predicted']:30s} | Confidence: {result['confidence']:.2%}")
        else:
            # Random case without known disease
            logger.info(f"  Case {result['case']:2d} [{result['type']:6s}]: Predicted: {result['predicted']:30s} | Confidence: {result['confidence']:.2%}")
    
    logger.info("\n" + "=" * 80)
    logger.success("✓ Inference tests completed!")
    logger.info("=" * 80)


if __name__ == "__main__":
    try:
        test_model_inference()
    except KeyboardInterrupt:
        logger.info("\nTest interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

