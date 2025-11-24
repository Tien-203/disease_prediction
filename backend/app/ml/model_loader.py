"""ML Model loader for loading trained models"""
import os
import joblib
from pathlib import Path
from loguru import logger
from typing import Optional, Any


class ModelLoader:
    """Class for loading and managing ML models"""
    
    def __init__(self):
        self.model: Optional[Any] = None
        self.label_encoder: Optional[Any] = None
        self.feature_names: Optional[list] = None
        self.group_encoders: Optional[dict] = None
        self._is_loaded = False
    
    def load_models(
        self,
        model_path: str,
        label_encoder_path: str,
        feature_names_path: str,
        group_encoders_path: Optional[str] = None
    ) -> bool:
        """
        Load ML models from disk
        
        Args:
            model_path: Path to the trained model file
            label_encoder_path: Path to the label encoder file
            feature_names_path: Path to the feature names file
            group_encoders_path: Optional path to group encoders file (for group-based models)
            
        Returns:
            bool: True if models loaded successfully, False otherwise
        """
        try:
            # Convert to absolute paths
            base_path = Path(__file__).parent.parent.parent
            model_path = base_path / model_path
            label_encoder_path = base_path / label_encoder_path
            feature_names_path = base_path / feature_names_path
            
            # Check if files exist
            if not model_path.exists():
                logger.warning(f"Model file not found: {model_path}")
                return False
            
            if not label_encoder_path.exists():
                logger.warning(f"Label encoder file not found: {label_encoder_path}")
                return False
            
            if not feature_names_path.exists():
                logger.warning(f"Feature names file not found: {feature_names_path}")
                return False
            
            # Load models
            logger.info(f"Loading model from {model_path}")
            self.model = joblib.load(model_path)
            
            logger.info(f"Loading label encoder from {label_encoder_path}")
            self.label_encoder = joblib.load(label_encoder_path)
            
            logger.info(f"Loading feature names from {feature_names_path}")
            self.feature_names = joblib.load(feature_names_path)
            
            # Load group encoders if provided (for group-based models)
            if group_encoders_path:
                group_encoders_path = base_path / group_encoders_path
                if group_encoders_path.exists():
                    logger.info(f"Loading group encoders from {group_encoders_path}")
                    self.group_encoders = joblib.load(group_encoders_path)
                    logger.info("Group encoders loaded successfully")
                else:
                    logger.warning(f"Group encoders file not found: {group_encoders_path}")
                    self.group_encoders = None
            else:
                self.group_encoders = None
            
            self._is_loaded = True
            logger.info("All models loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self._is_loaded = False
            return False
    
    def is_loaded(self) -> bool:
        """Check if models are loaded"""
        return self._is_loaded
    
    def get_model(self):
        """Get the loaded model"""
        if not self._is_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.model
    
    def get_label_encoder(self):
        """Get the loaded label encoder"""
        if not self._is_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.label_encoder
    
    def get_feature_names(self):
        """Get the feature names"""
        if not self._is_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.feature_names
    
    def get_group_encoders(self):
        """Get the group encoders (for group-based models)"""
        if not self._is_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.group_encoders


# Global model loader instance
model_loader = ModelLoader()

