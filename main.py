import json
from core.config import get_settings
import pandas as pd
import requests


settings = get_settings()    


url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"

querystring = {"league":"39","season":"2020"}

headers = {
	"x-rapidapi-key": "de5bd5b5b7msha460bb7d261f1b1p1fe289jsncc96fb44fa60",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json().get('results'))
