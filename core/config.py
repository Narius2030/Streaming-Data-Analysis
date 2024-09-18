import sys
import os
from pathlib import Path
from dotenv import load_dotenv
sys.path.append('./')
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings():
    # Database
    ELASTIC_HOST: str = os.getenv('ELASTIC_HOST')
    # APIs
    TMDB_BEARER_TOKEN: str = os.getenv('TMDB_BEARER_TOKEN')
    FILMS_INDEX_KEY: str = os.getenv('FILMS_INDEX_KEY')
    
def get_settings() -> Settings:
    return Settings()