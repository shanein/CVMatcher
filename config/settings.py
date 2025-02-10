import os
from dotenv import load_dotenv

load_dotenv('.env')

API_KEY = os.getenv("MISTRAL_API_KEY")
# MODEL_NAME = "mistral-large-latest"
