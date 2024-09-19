import json
from core.config import get_settings
import pandas as pd
import requests


settings = get_settings()    

url = f"https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}"
}
response = requests.get(url, headers=headers)
print(response.json().get('results'))
