import sys
sys.path.append('./')

from functions.KafkaComponent import Consumer, Producer
import time
import json
import requests
from datetime import date
from core.config import get_settings
from functions.ElasticHandler import ElasticHandlers


settings = get_settings()

def request_movies():
    stop_event = False
    for page in range(1,6):
        # TODO: recieve data from API sources - transformation is optional
        url = f"https://api.themoviedb.org/3/movie/now_playing?language=en-US&page={page}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        if page == 5:
            stop_event = True
        yield (response.json().get('results'), response.json().get('page'), stop_event)
    

def request_tvseries():
    stop_event = False
    for page in range(1,6):
        # TODO: recieve data from API sources - transformation is optional
        url = f"https://api.themoviedb.org/3/tv/airing_today?language=en-US&page={page}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        if page == 5:
            stop_event = True
        yield (response.json().get('results'), response.json().get('page'), stop_event)


def write_logs(message, path):
    # Filter value
    for _, datas in message.items():
        for data in datas:
            # write data into json
            value = data.value.decode('utf-8')
            value = json.loads(value)
            print(value)
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

    try:
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
        print("Films transporting threads have stopped ✔")
    except Exception as exc:
        print(str(exc) + '❌')
    
if __name__=='__main__':
    topic_name='films'
    
    ## TODO: run transporting
    transport(topic_name)
    
    ## TODO: data processing functions
    # handler = ElasticHandlers(
    #     host=settings.ELASTIC_HOST,
    #     api_key=settings.FILMS_INDEX_KEY,
    # )
    # documents = handler.create_documents(index=topic_name, path="./logs/*.json")
    # handler.ingest_data(es, "films", documents)
