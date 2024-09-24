import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
sys.path.append('./')
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # Database
    ELASTIC_HOST: str = os.getenv('ELASTIC_HOST')
    # APIs
    TMDB_BEARER_TOKEN: str = os.getenv('TMDB_BEARER_TOKEN')
    SPORT_RK_TOKEN: str = os.getenv('SPORT_RK_TOKEN')
    TMDB_INDEX_KEY: str = os.getenv('TMDB_INDEX_KEY')
    SPORT_RK_INDEX_KEY: str = os.getenv('SPORT_RK_INDEX_KEY')
    
def get_settings() -> Settings:
    return Settings()