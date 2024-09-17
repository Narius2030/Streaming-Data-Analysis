import sys
sys.path.append('./')

from functions.KafkaComponent import Consumer, Producer
import time
import json
import requests
from datetime import datetime, date
from core.config import get_settings

settings = get_settings()

def request_movies(page):
    # TODO: recieve data from API sources - transformation is optional
    ### START CODE HERE
    url = f"https://api.themoviedb.org/3/movie/now_playing?language=en-US&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    return response.json().get('results')
    ### END CODE HERE
    

def request_tvseries(page):
    # TODO: recieve data from API sources - transformation is optional
    ### START CODE HERE
    url = f"https://api.themoviedb.org/3/tv/airing_today?language=en-US&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    return response.json().get('results')
    ### END CODE HERE


def write_logs(message, path):
    # Filter value
    for _, datas in message.items():
        for data in datas:
            # write data into json
            value = data.value.decode('utf-8')
            value = json.loads(value)
            with open(f"{path}/{value['type']}_{date.today()}_{value['page']}.json", "w", encoding="utf-8") as file:
                json.dump(value, file, indent=4)

def transport(topic):
    prod_tasks = [
        Producer(topic=topic, function=request_movies, key='movie'),
        Producer(topic=topic, function=request_tvseries, key='tvseries'),
    ]
    
    cons_tasks = [
        Consumer(topic=topic, group_id='films', path='./logs', function=write_logs),
        Consumer(topic=topic, group_id='films', path='./logs', function=write_logs)
    ]

    # Start threads and Stop threads
    for t in prod_tasks:
        t.start()
    time.sleep(2)
    for task in prod_tasks:
        task.stop()
    
    for t in cons_tasks:
        t.start()
    time.sleep(5)
    for task in cons_tasks:
        task.stop()
        
    for task in prod_tasks:
        task.join()
    for task in cons_tasks:
        task.join()
    
    print("Threads have stopped.")
    
    
if __name__=='__main__':
    # topics
    topic_name='films'
    
    # run transporting
    transport(topic_name)
    
    # data processing functions
    ...
