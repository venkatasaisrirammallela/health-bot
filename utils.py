import os
from dotenv import load_dotenv
import re
from typing import Union, Optional

# Load environment variables
load_dotenv()

def get_api_key() -> str:
    """Get the Google API key from environment variables."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    return api_key

def validate_age(age_input: str) -> tuple[bool, Optional[int]]:
    """
    Validate age input.
    Returns (is_valid, age_value)
    """
    try:
        age = int(age_input)
        if age < 0 or age > 120:  # Reasonable age range
            return False, None
        return True, age
    except ValueError:
        return False, None

def validate_temperature(temp_input: str) -> tuple[bool, Optional[float]]:
    """
    Validate temperature input.
    Returns (is_valid, temperature_value)
    """
    try:
        temp = float(temp_input)
        if temp < 35.0 or temp > 42.0:  # Reasonable temperature range in Celsius
            return False, None
        return True, temp
    except ValueError:
        return False, None

def validate_yes_no(input_text: str) -> Optional[bool]:
    """
    Validate yes/no input.
    Returns True for yes, False for no, None for invalid input.
    """
    input_text = input_text.lower().strip()
    if input_text in ['yes', 'y', 'true', '1']:
        return True
    if input_text in ['no', 'n', 'false', '0']:
        return False
    return None

def format_symptom_summary(symptoms: dict) -> str:
    """Format collected symptoms into a readable summary."""
    summary = "Collected Symptoms:\n"
    for key, value in symptoms.items():
        summary += f"- {key.replace('_', ' ').title()}: {value}\n"
    return summary

def clean_text(text: str) -> str:
    """Clean and normalize input text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    # Convert to lowercase
    text = text.lower()
    return text

def format_ml_prediction(prediction: str, confidence: float) -> str:
    """Format ML model prediction with confidence score."""
    return f"Preliminary Assessment: {prediction}\nConfidence: {confidence:.1%}" 