"""Prediction logic for disease prediction"""
import numpy as np
from typing import List, Tuple
from loguru import logger
from app.ml.model_loader import ModelLoader
from app.ml.preprocessor import DataPreprocessor


class DiseasePredictor:
    """Class for making disease predictions"""
    
    def __init__(self, model_loader: ModelLoader):
        """
        Initialize predictor with model loader
        
        Args:
            model_loader: Instance of ModelLoader with loaded models
        """
        self.model_loader = model_loader
        group_encoders = model_loader.get_group_encoders()
        self.preprocessor = DataPreprocessor(
            model_loader.get_feature_names(),
            group_encoders=group_encoders
        )
    
    def predict(self, symptoms: List[str]) -> Tuple[str, float, List[Tuple[str, float]]]:
        """
        Predict disease based on symptoms
        
        Args:
            symptoms: List of symptom names
            
        Returns:
            tuple: (predicted_disease, confidence, alternatives)
                - predicted_disease: Name of the predicted disease
                - confidence: Confidence score (0-1)
                - alternatives: List of (disease, confidence) tuples for alternatives
        """
        if not self.model_loader.is_loaded():
            raise RuntimeError("ML models not loaded")
        
        # Preprocess symptoms
        feature_vector = self.preprocessor.preprocess_symptoms(symptoms)
        
        # Get model and label encoder
        model = self.model_loader.get_model()
        label_encoder = self.model_loader.get_label_encoder()
        
        # Make prediction
        prediction = model.predict(feature_vector)[0]
        predicted_disease = label_encoder.inverse_transform([prediction])[0]
        
        # Get prediction probabilities
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(feature_vector)[0]
            confidence = float(probabilities[prediction])
            
            # Get top 3 alternatives
            top_indices = np.argsort(probabilities)[::-1][:4]  # Top 4 including the prediction
            alternatives = []
            
            for idx in top_indices[1:]:  # Skip the first one (it's the main prediction)
                disease = label_encoder.inverse_transform([idx])[0]
                prob = float(probabilities[idx])
                if prob > 0.01:  # Only include if probability > 1%
                    alternatives.append((disease, prob))
        else:
            confidence = 1.0
            alternatives = []
        
        logger.info(
            f"Predicted disease: {predicted_disease} "
            f"(confidence: {confidence:.2%})"
        )
        
        return predicted_disease, confidence, alternatives
    
    def get_matched_symptoms(self, symptoms: List[str]) -> Tuple[List[str], List[str]]:
        """
        Get matched and unmatched symptoms
        
        Args:
            symptoms: List of symptom names
            
        Returns:
            tuple: (matched_symptoms, unmatched_symptoms)
        """
        return self.preprocessor.get_matched_symptoms(symptoms)

