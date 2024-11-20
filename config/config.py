import os
from dotenv import load_dotenv

def load_config():
    """Load configuration from environment variables"""
    load_dotenv()
    
    config = {
        'serpapi_key': os.getenv('SERPAPI_KEY'),
        'huggingface_api_key': os.getenv('HUGGINGFACE_API_KEY'),
        'google_credentials': os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    }
    
    return config