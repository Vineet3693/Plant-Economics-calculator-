
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GROQ_MODEL = "llama-3.1-70b-versatile"
    
    # Application Settings
    APP_TITLE = "Plant Economics Calculator"
    APP_ICON = "🏭"
    
    # Default Values
    DEFAULT_INTEREST_RATE = 10.0
    DEFAULT_PROJECT_LIFE = 10
    DEFAULT_SALVAGE_RATE = 10.0
    
    # Styling
    PRIMARY_COLOR = "#1f77b4"
    SECONDARY_COLOR = "#ff7f0e"
    SUCCESS_COLOR = "#2ca02c"
    WARNING_COLOR = "#ff7f0e"
    ERROR_COLOR = "#d62728"
    
    # Chart Configuration
    CHART_HEIGHT = 400
    CHART_WIDTH = 600
