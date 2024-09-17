import sys
sys.path.append('./')

from functions.KafkaComponent import Consumer, Producer
import time
import json
import requests
from datetime import datetime
from core.config import get_settings
    

settings = get_settings()

def request_data(page):
    # TODO: recieve data from API sources - transformation is optional
    ### START CODE HERE
    url = f"https://api.themoviedb.org/3/movie/now_playing?language=en-US&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    return response.json().get('results'), response.json().get('page')
    ### END CODE HERE


def write_logs(message, path, announce):
    # Filter value
    for _, datas in message.items():
        for data in datas:
            with open(path, 'a', encoding="utf-8") as file:
                # for data in datas:
                value = data.value.decode('utf-8')
                value = json.loads(value)
                file.write(f'{value} - {datetime.now()} - {announce}')

def example(topic):
    prod_tasks = [
        Producer(topic=topic, function=request_data),
    ]
    
    cons_tasks = [
        Consumer(topic=topic, group_id='movie', announce='writed from Consumer-01 movie-01\n', path='./logs/log01.txt', function=write_logs),
        Consumer(topic=topic, group_id='tv', announce='writed from Consumer-02 tv-01\n', path='./logs/log02.txt', function=write_logs)
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
    # topic and producer
    topic_name='films'
    
    # run main
    example(topic_name)