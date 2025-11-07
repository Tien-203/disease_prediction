"""Data preprocessing for ML predictions"""
import numpy as np
from typing import List
from loguru import logger


class DataPreprocessor:
    """Class for preprocessing input data for ML model"""
    
    def __init__(self, feature_names: List[str]):
        """
        Initialize preprocessor with feature names
        
        Args:
            feature_names: List of feature names expected by the model
        """
        self.feature_names = feature_names
        logger.info(f"Preprocessor initialized with {len(feature_names)} features")
    
    def preprocess_symptoms(self, symptoms: List[str]) -> np.ndarray:
        """
        Preprocess symptoms into feature vector
        
        Args:
            symptoms: List of symptom names
            
        Returns:
            np.ndarray: Feature vector for the model
        """
        # Create binary feature vector
        feature_vector = np.zeros(len(self.feature_names))
        
        # Convert symptom names to lowercase for matching
        symptoms_lower = [s.lower().strip().replace('_', ' ') for s in symptoms]
        
        # Set 1 for present symptoms
        for i, feature_name in enumerate(self.feature_names):
            feature_name_normalized = feature_name.lower().strip().replace('_', ' ')
            if feature_name_normalized in symptoms_lower:
                feature_vector[i] = 1
        
        logger.debug(f"Preprocessed {len(symptoms)} symptoms into feature vector")
        return feature_vector.reshape(1, -1)
    
    def get_matched_symptoms(self, symptoms: List[str]) -> tuple[List[str], List[str]]:
        """
        Get matched and unmatched symptoms
        
        Args:
            symptoms: List of input symptom names
            
        Returns:
            tuple: (matched_symptoms, unmatched_symptoms)
        """
        symptoms_lower = [s.lower().strip().replace('_', ' ') for s in symptoms]
        feature_names_lower = [f.lower().strip().replace('_', ' ') for f in self.feature_names]
        
        matched = []
        unmatched = []
        
        for symptom in symptoms:
            symptom_normalized = symptom.lower().strip().replace('_', ' ')
            if symptom_normalized in feature_names_lower:
                matched.append(symptom)
            else:
                unmatched.append(symptom)
        
        return matched, unmatched

