from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

try:
    load_dotenv()
except OSError:
    load_dotenv('.')

class Settings(BaseSettings):
    # Configuration for the database
    DATABASE_URL: str = os.getenv('DATABASE_URL')

    # Configuration for FastAPI
    API_PREFIX: str = '/'
    VERSION: str = 'v1'
    PROJECT_NAME: str = os.getenv('PROJECT_NAME')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Configuration for Cloud ANPR API
    ANPR_API_ENDPOINT: str = os.getenv('ANPR_API_ENDPOINT')
    ANPR_API_USER: str = os.getenv('ANPR_API_USER')
    ANPR_API_PASSWORD: str = os.getenv('ANPR_API_PASSWORD')

    # Other configurations

settings = Settings()
