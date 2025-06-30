import os
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Initialize Anthropic client
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    print("Warning: ANTHROPIC_API_KEY not found in environment variables")
    anthropic_client = None
else:
    try:
        anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        print("Anthropic client initialized successfully")
    except Exception as e:
        print(f"Error initializing Anthropic client: {e}")
        anthropic_client = None

# CORS origins
CORS_ORIGINS = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173", 
    "http://localhost:5174", 
    "http://127.0.0.1:5174",
    "http://localhost:5175", 
    "http://127.0.0.1:5175"
]
