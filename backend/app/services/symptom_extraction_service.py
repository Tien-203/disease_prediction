"""Service for extracting symptoms from natural language using LangChain and Gemini"""
import json
import os
import re
from typing import List
from loguru import logger

from app.core.config import settings


class SymptomExtractionService:
    """Service for extracting predefined symptoms from natural language descriptions"""
    
    def __init__(self):
        """Initialize the service with reference data"""
        self.reference_data_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "db",
            "reference_data.json"
        )
        self.reference_data = self._load_reference_data()
        self.available_symptoms = self.reference_data.get("symptoms", [])
        
    def _load_reference_data(self) -> dict:
        """Load reference data from JSON file"""
        try:
            with open(self.reference_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading reference data: {str(e)}")
            return {"symptoms": []}
    
    def extract_symptoms(self, natural_language: str) -> List[str]:
        """
        Extract predefined symptoms from natural language description using Gemini
        
        Args:
            natural_language: Natural language description of symptoms
            
        Returns:
            List of predefined symptom names that match the description
        """
        if not settings.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY not configured")
            raise ValueError("Gemini API key is not configured. Please set GEMINI_API_KEY in .env file")
        
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            # Initialize Gemini model
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.1
            )
            
            # Create simple prompt
            symptoms_list = ", ".join(self.available_symptoms)
            prompt = f"""You are a medical assistant. Extract symptoms from the patient's description and map them to predefined symptoms.

Available predefined symptoms: {symptoms_list}

Patient description: {natural_language}

Instructions:
- Identify all symptoms mentioned
- Map to exact predefined symptom names (use underscores, not spaces)
- Return ONLY a JSON array of symptom names
- Example: ["headache", "dizziness", "high_fever"]

Return only the JSON array:"""
            
            # Get response
            logger.info(f"Extracting symptoms from: {natural_language[:100]}...")
            response = llm.invoke(prompt)
            response_text = response.content.strip()
            
            # Clean and parse JSON
            response_text = re.sub(r'```json\s*', '', response_text)
            response_text = re.sub(r'```\s*', '', response_text)
            response_text = response_text.strip()
            
            # Extract JSON array
            array_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if array_match:
                response_text = array_match.group()
            
            # Parse JSON
            try:
                extracted_symptoms = json.loads(response_text)
                if not isinstance(extracted_symptoms, list):
                    extracted_symptoms = []
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON: {response_text}")
                extracted_symptoms = []
            
            # Validate symptoms are in predefined list
            valid_symptoms = [
                symptom for symptom in extracted_symptoms
                if symptom in self.available_symptoms
            ]
            
            logger.info(f"Extracted {len(valid_symptoms)} valid symptoms: {valid_symptoms}")
            return valid_symptoms
            
        except ImportError as e:
            logger.error(f"Required packages not installed: {str(e)}")
            raise ValueError("LangChain packages not installed. Run: uv add langchain langchain-google-genai")
        except Exception as e:
            logger.error(f"Error extracting symptoms: {str(e)}")
            raise ValueError(f"Failed to extract symptoms: {str(e)}")

