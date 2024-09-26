import sys
sys.path.append('./')

from functions.KafkaComponent import Consumer, Producer
import time
import glob
from core.config import get_settings
from functions.ElasticHandler import ElasticHandlers
from src.publishes import request_movies, request_tvseries, request_sport_ranking
from src.subscribes import write_json_logs


settings = get_settings()

def transport():
    prod_tasks = [
        Producer(topic="films", generator=request_movies, key='movie'),
        Producer(topic="films", generator=request_tvseries, key='tvseries'),
        Producer(topic="sports", generator=request_sport_ranking, key='sport_ranking'),
    ]
    
    cons_tasks = [
        Consumer(topic="films", group_id='films', path='./logs', function=write_json_logs),
        Consumer(topic="films", group_id='films', path='./logs', function=write_json_logs),
        Consumer(topic="sports", group_id='sports' , path='./logs', function=write_json_logs),
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
    ## TODO: run transporting
    transport()
    
    ## TODO: insert data to tmdb-index
    handler = ElasticHandlers(
        host=settings.ELASTIC_HOST,
        api_key=settings.TMDB_INDEX_KEY,
    )
    filepathes = glob.glob("./logs/movie*.json") + glob.glob("./logs/tvseries*.json")
    documents = handler.create_documents(index='films', filepathes=filepathes)
    
    updatable_fields = ['popularity','vote_average','vote_count']
    handler.ingest_data(index="tmdb-index", updatable_fields=updatable_fields, documents=documents, string_id='id')
    
    ## TODO: insert data to sport-ranking
    handler = ElasticHandlers(
        host=settings.ELASTIC_HOST,
        api_key=settings.SPORT_RK_INDEX_KEY,
    )
    filepathes = glob.glob("./logs/sport_ranking*.json")
    documents = handler.create_documents(index="sport-ranking", filepathes=filepathes)
    
    updatable_fields = ['current_ranking','current_points','previous_ranking', 'previous_points', 'growth_point']
    handler.ingest_data(index="sport-ranking", updatable_fields=updatable_fields, documents=documents, string_id='nameCode')
