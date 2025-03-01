 
# # config.py

# import os

# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
#     MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://lahiru:8233001696@cluster0.v1mwx.mongodb.net/')


import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')
    MONGO_URI = os.getenv('MONGO_URI')
    
    # Add a print statement for debugging
    print(f"MONGO_URI: {MONGO_URI}")

