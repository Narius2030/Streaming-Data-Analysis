import sys
sys.path.append('./')

from functions.KafkaComponent import Consumer, Producer
from functions.ElasticHandler import ElasticHandlers
from core.config import get_settings
import time
import json
from datetime import date
import http.client


settings = get_settings()

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
            # data_json['page'] = page
        except Exception as exc:
            raise Exception(str(exc))
        yield (data_json, page) #json.dumps(get_ranking(data_json), indent=4, ensure_ascii=False)


def get_ranking(data_json):
    # Danh sách để lưu trữ tất cả các thông điệp
    all_messages = []
    
    # Kiểm tra nếu dữ liệu hợp lệ
    if isinstance(data_json, dict) and 'rankings' in data_json:
        for ranking_item in data_json['rankings']:
            team = ranking_item['team']
            message = {
                'page': data_json['page'],
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

def write_logs(message, path):
    # Filter value
    for _, datas in message.items():
        for data in datas:
            # write data into json
            value = data.value.decode('utf-8')
            value = json.loads(value)
            with open(f"{path}/{value['type']}_{date.today()}_{value['page']}.json", "w", encoding="utf-8") as file:
                json.dump(value, file, indent=4)

def example(topic):
    prod_tasks = [
        Producer(topic=topic, function=request_sport_ranking, key='sport_ranking'),
    ]
    
    cons_tasks = [
        Consumer(topic=topic, group_id='sports' , path='./logs', function=write_logs),
        # Consumer(topic=topic, group_id='sports' , path='./logs', function=write_logs),
    ]

    # Start threads and Stop threads
    for t in prod_tasks:
        t.start()
    time.sleep(2)
    
    for t in cons_tasks:
        t.start()
    time.sleep(5)
   

    for task in prod_tasks:
        task.stop()
    for task in cons_tasks:
        task.stop()

    for task in prod_tasks:
        task.join()
    for task in cons_tasks:
        task.join()
    
    print("Thread of Consumber has stopped.")
    
    
if __name__=='__main__':
    # topic and producer
    topic_name='sports'
    
    # run main
    # example(topic_name)

    # insert data to Elastic    
    handler = ElasticHandlers(
        host=settings.ELASTIC_HOST,
        api_key=settings.SPORT_RK_INDEX_KEY,
    )
    documents = handler.create_documents(index="sport-ranking", path="./logs/sport_ranking_*.json")
    print(documents[0])
    handler.ingest_data(index="sport-ranking", documents=documents)
    
