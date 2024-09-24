import json
from core.config import get_settings
import pandas as pd
import requests
import http.client
import glob
from pathlib import Path


settings = get_settings()    

files = list(Path("./logs/").glob("**/(movie|tvseries)*.json"))
files = glob.glob("./logs/movie*.json") + glob.glob("./logs/tvseries*.json")
print(files)