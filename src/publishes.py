import sys
sys.path.append('./')

import requests
import http.client
import json
from core.config import get_settings


settings = get_settings()


def request_movies():
    # TODO: recieve data from API sources - transformation is optional
    stop_event = False
    for page in range(1,6):
        try:
            url = f"https://api.themoviedb.org/3/movie/now_playing?language=en-US&page={page}"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}"
            }
            response = requests.get(url, headers=headers)
            data = response.json().get('results')
            page = response.json().get('page')
            if page == 5:
                stop_event = True
        except Exception as exc:
            raise Exception(str(exc))
        yield (data, page, stop_event)
    

def request_tvseries():
    # TODO: recieve data from API sources - transformation is optional
    stop_event = False
    for page in range(1,6):
        try:
            url = f"https://api.themoviedb.org/3/tv/airing_today?language=en-US&page={page}"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}"
            }
            response = requests.get(url, headers=headers)
            data = response.json().get('results')
            page = response.json().get('page')
            if page == 5:
                stop_event = True
        except Exception as exc:
            raise Exception(str(exc))
        yield (data, page, stop_event)
        
        
def get_ranking(data_json):
    # Danh sách để lưu trữ tất cả các thông điệp
    all_messages = []
    
    # Kiểm tra nếu dữ liệu hợp lệ
    if isinstance(data_json, dict) and 'rankings' in data_json:
        for ranking_item in data_json['rankings']:
            team = ranking_item['team']
            message = {
                'name': team['name'],
                'nameCode': team['nameCode'],
                'current_ranking': ranking_item['ranking'],
                'current_points': ranking_item.get('points', None),
                'previous_ranking': ranking_item.get('previousRanking', None),
                'previous_points': ranking_item.get('previousPoints', None),
                'growth_point': (ranking_item.get('points', None) - ranking_item.get('previousPoints', None))
            }
            # Thêm thông điệp vào danh sách
            all_messages.append(message)
    return all_messages


def request_sport_ranking():
    for page in range(1, 2):
        try:
            # TODO: recieve data from API sources - transformation is optional    
            conn = http.client.HTTPSConnection("footapi7.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': "a7f9745956msh7d364da5b308313p198455jsn24af2af221ef",
                'x-rapidapi-host': "footapi7.p.rapidapi.com"
            }
            conn.request("GET", "/api/rankings/fifa", headers=headers)
            res = conn.getresponse()
            data = res.read()
            # Chuyển đổi dữ liệu từ byte sang chuỗi và sau đó thành đối tượng JSON
            data_json = json.loads(data.decode("utf-8"))
            data = get_ranking(data_json)
        except Exception as exc:
            raise Exception(str(exc))
        yield (data, page)