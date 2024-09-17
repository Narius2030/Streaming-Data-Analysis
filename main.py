import requests
from core.config import get_settings


settings = get_settings()    

url = f"https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}"
}
response = requests.get(url, headers=headers)
response = dict(response.json())
results = response.get('results')
key = response['page']

print(results)