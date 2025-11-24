"""Data preprocessing for ML predictions"""
import numpy as np
from typing import List, Dict
from loguru import logger


class DataPreprocessor:
    """Class for preprocessing input data for ML model"""
    
    def __init__(self, feature_names: List[str], group_encoders: dict = None):
        """
        Initialize preprocessor with feature names
        
        Args:
            feature_names: List of feature names expected by the model (should be group names if using group-based model)
            group_encoders: Optional dictionary of group encoders for encoding symptom names
        """
        self.feature_names = feature_names
        self.group_encoders = group_encoders
        self.group_mapping = self._get_group_mapping()
        logger.info(f"Preprocessor initialized with {len(feature_names)} group-based features")
        if self.group_encoders:
            logger.info("Group encoders available for encoding symptom names")
    
    def _get_group_mapping(self) -> Dict[str, List[str]]:
        """
        Get mapping of symptom keywords to groups
        This matches the grouping logic in symptom_service.py and preprocess_data_with_groups.py
        
        Returns:
            Dictionary mapping group names to keyword lists
        """
        return {
            "pain": ["pain", "ache", "cramp", "sore"],
            "respiratory": ["cough", "breath", "sneezing", "congestion", "phlegm", "sputum", "runny_nose", "throat"],
            "fever": ["fever", "chills", "shivering", "sweating"],
            "digestive": ["abdominal", "belly", "stomach", "nausea", "vomiting", "diarrhoea", "constipation", "indigestion", "acidity", "gas"],
            "urinary": ["urine", "urination", "bladder", "micturition", "polyuria"],
            "skin": ["rash", "itching", "blister", "eruption", "patches", "peeling", "yellowish_skin", "redness", "blackheads", "pimples"],
            "neurological": ["headache", "dizziness", "vertigo", "loss_of_balance", "unsteadiness", "slurred_speech", "coma", "altered_sensorium", "weakness", "paralysis"],
            "vision": ["vision", "eyes", "blurred", "redness_of_eyes", "watering_from_eyes", "yellowing_of_eyes", "sunken_eyes"],
            "energy": ["fatigue", "lethargy", "weakness", "malaise", "loss_of_appetite", "excessive_hunger", "increased_appetite"],
            "mental": ["anxiety", "depression", "irritability", "mood_swings", "restlessness", "lack_of_concentration"],
            "joint_muscle": ["joint", "muscle", "knee", "hip", "neck", "back", "stiffness", "swelling", "movement"],
            "appetite_weight": ["appetite", "weight", "obesity", "loss_of_appetite", "increased_appetite", "excessive_hunger"]
        }
    
    def _map_symptom_to_group(self, symptom_name: str) -> str:
        """
        Map a symptom name to its group
        
        Args:
            symptom_name: Name of the symptom
            
        Returns:
            Group name or "other" if no match found
        """
        if not self.group_mapping:
            return "other"
        
        symptom_lower = symptom_name.lower().strip().replace(' ', '_')
        
        # Check each category
        for group_name, keywords in self.group_mapping.items():
            # Check if any keyword matches the symptom name
            if any(keyword in symptom_lower for keyword in keywords):
                return group_name
        
        # If no match, return "other"
        return "other"
    
    def preprocess_symptoms(self, symptoms: List[str]) -> np.ndarray:
        """
        Preprocess symptoms into feature vector
        If using group-based model, maps symptoms to groups first
        
        Args:
            symptoms: List of symptom names
            
        Returns:
            np.ndarray: Feature vector for the model
        """
        # Create feature vector for group-based model
        feature_vector = np.zeros(len(self.feature_names))
        
        # Map symptoms to groups and collect symptom names per group
        group_symptoms: Dict[str, List[str]] = {group: [] for group in self.feature_names}
        
        for symptom in symptoms:
            group = self._map_symptom_to_group(symptom)
            if group in group_symptoms:
                group_symptoms[group].append(symptom)
        
        # Encode each group's symptoms
        for i, feature_name in enumerate(self.feature_names):
            group = feature_name.lower()
            if group_symptoms[group]:
                # Normalize and sort symptoms to ensure consistent format
                # This matches the format used during training
                # Important: normalize exactly like preprocessing script
                normalized_symptoms = []
                for s in group_symptoms[group]:
                    # Normalize: strip, lowercase, and replace spaces with underscores
                    normalized = s.strip().lower().replace(' ', '_')
                    if normalized:
                        normalized_symptoms.append(normalized)
                normalized_symptoms = sorted(set(normalized_symptoms))  # Sort and remove duplicates
                symptom_string = ','.join(normalized_symptoms)
                
                # Encode using group encoder if available
                if self.group_encoders and group in self.group_encoders:
                    encoder = self.group_encoders[group]
                    
                    # Debug: log encoder classes for this group
                    logger.info(f"Group '{group}': trying to encode '{symptom_string}'")
                    logger.info(f"  Available encoder classes ({len(encoder.classes_)}): {list(encoder.classes_[:5])}")
                    
                    # Check if symptom_string has spaces
                    if ' ' in symptom_string:
                        logger.warning(f"  ⚠️  Symptom string has spaces: '{symptom_string}'")
                    
                    # Check encoder classes for spaces
                    classes_with_spaces = [cls for cls in encoder.classes_ if ' ' in cls]
                    if classes_with_spaces:
                        logger.warning(f"  ⚠️  Found {len(classes_with_spaces)} encoder classes with spaces!")
                        logger.warning(f"  Examples: {classes_with_spaces[:3]}")
                    
                    # Try to find matching combination in encoder classes
                    # First try exact match
                    if symptom_string in encoder.classes_:
                        logger.info(f"  ✓ Found exact match: '{symptom_string}'")
                        try:
                            encoded_value = encoder.transform([symptom_string])[0]
                            feature_vector[i] = encoded_value
                        except (ValueError, KeyError):
                            feature_vector[i] = 0
                    else:
                        # Try to find partial matches or use most common encoding
                        # Normalize encoder classes for comparison (handle spaces)
                        found_match = False
                        for encoder_class in encoder.classes_:
                            # Normalize encoder class symptoms the same way
                            encoder_symptom_list = [s.strip().lower().replace(' ', '_') for s in encoder_class.split(',')]
                            encoder_symptom_set = set(encoder_symptom_list)
                            
                            if encoder_symptom_set == set(normalized_symptoms):
                                # Found exact match (same symptoms, possibly different order or format)
                                try:
                                    encoded_value = encoder.transform([encoder_class])[0]
                                    feature_vector[i] = encoded_value
                                    found_match = True
                                    logger.info(f"  ✓ Found match (normalized): '{symptom_string}' matches '{encoder_class}' in group '{group}'")
                                    break
                                except (ValueError, KeyError):
                                    continue
                        
                        if not found_match:
                            # Try to find best partial match (subset with most symptoms)
                            best_match_score = 0
                            best_match_value = 0
                            best_match_class = None
                            
                            for encoder_class in encoder.classes_:
                                # Normalize encoder class symptoms
                                encoder_symptom_list = [s.strip().lower().replace(' ', '_') for s in encoder_class.split(',')]
                                encoder_symptom_set = set(encoder_symptom_list)
                                
                                # Calculate overlap
                                overlap = len(encoder_symptom_set.intersection(set(normalized_symptoms)))
                                if overlap > best_match_score and overlap > 0:
                                    best_match_score = overlap
                                    try:
                                        best_match_value = encoder.transform([encoder_class])[0]
                                        best_match_class = encoder_class
                                    except:
                                        continue
                            
                            if best_match_score > 0:
                                feature_vector[i] = best_match_value
                                logger.info(f"  ⚠️  Using partial match for '{symptom_string}' in group '{group}' (overlap: {best_match_score}/{len(normalized_symptoms)})")
                                logger.info(f"     Matched with: '{best_match_class}'")
                            else:
                                # No match found, use 0 as fallback
                                logger.error(f"❌ Symptom combination '{symptom_string}' not found in group '{group}' encoder!")
                                logger.error(f"  Available classes: {len(encoder.classes_)}")
                                logger.error(f"  Sample classes: {list(encoder.classes_[:5])}")
                                logger.error(f"  Input symptoms: {group_symptoms[group]}")
                                logger.error(f"  Normalized: {normalized_symptoms}")
                                logger.error(f"  Symptom string: '{symptom_string}'")
                                feature_vector[i] = 0
                else:
                    # No encoder available, use binary (1 if has symptoms, 0 otherwise)
                    feature_vector[i] = 1
            else:
                # No symptoms in this group - use 'nan' encoding if available (matches training behavior)
                # During training, NaN values become 'nan' string when converted to str
                if self.group_encoders and group in self.group_encoders:
                    encoder = self.group_encoders[group]
                    if 'nan' in encoder.classes_:
                        try:
                            feature_vector[i] = encoder.transform(['nan'])[0]
                            logger.debug(f"Group '{group}': encoded 'nan' as {feature_vector[i]}")
                        except (ValueError, KeyError):
                            feature_vector[i] = 0
                    else:
                        # If 'nan' not in encoder, use 0 (shouldn't happen if model trained correctly)
                        feature_vector[i] = 0
                        logger.debug(f"Group '{group}': 'nan' not in encoder classes, using 0")
                else:
                    feature_vector[i] = 0
        
        logger.info(f"Preprocessed {len(symptoms)} symptoms into groups")
        logger.info(f"Feature vector: {feature_vector.flatten()}")
        logger.info(f"Non-zero features: {np.count_nonzero(feature_vector)}/{len(feature_vector)}")
        
        # Log which groups have non-zero values
        non_zero_groups = []
        for i, feature_name in enumerate(self.feature_names):
            if feature_vector[i] != 0:
                non_zero_groups.append(f"{feature_name}={feature_vector[i]}")
        if non_zero_groups:
            logger.info(f"Non-zero groups: {', '.join(non_zero_groups)}")
        else:
            logger.error("⚠️  ALL FEATURES ARE ZERO! This will cause default prediction.")
        
        # Convert to integer type (encoded values are integers) and reshape for model
        # Model expects shape (1, n_features) with integer-encoded values
        feature_vector = feature_vector.astype(np.int64).reshape(1, -1)
        return feature_vector
    
    def get_matched_symptoms(self, symptoms: List[str]) -> tuple[List[str], List[str]]:
        """
        Get matched and unmatched symptoms
        All symptoms that map to a group are considered matched
        
        Args:
            symptoms: List of input symptom names
            
        Returns:
            tuple: (matched_symptoms, unmatched_symptoms)
        """
        matched = []
        unmatched = []
        
        for symptom in symptoms:
            group = self._map_symptom_to_group(symptom)
            if group in [f.lower() for f in self.feature_names]:
                matched.append(symptom)
            else:
                unmatched.append(symptom)
        
        return matched, unmatched

