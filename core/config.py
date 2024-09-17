import sys
import os
from pathlib import Path
from dotenv import load_dotenv
sys.path.append('./')
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings():
    # Database
    DB_USER: str = os.getenv('MONGO_ATLAS_USER')
    DB_PASSWORD: str = os.getenv('MONGO_ATLAS_PASSWD')
    DB_NAME: str = os.getenv('MONGO_ATLAS_DB')
    DB_HOST: str = os.getenv('MONGO_ATLAS_HOST')
    DB_CLUSTER: str = os.getenv('MONGO_ATLAS_CLUSTER')
    DATABASE_URL: str = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/?retryWrites=true&w=majority&appName={DB_CLUSTER}"
    
    # APIs
    TMDB_BEARER_TOKEN: str = os.getenv('TMDB_BEARER_TOKEN')
    
def get_settings() -> Settings:
    return Settings()