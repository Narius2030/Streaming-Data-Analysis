import sys
sys.path.append('./')

from functions.KafkaComponent import Consumer, Producer
import time
import json
from datetime import date, datetime


def request_data():
    # TODO: recieve data from API sources - transformation is optional
    ### CODE HERE
    
    ### CODE HERE
    pass


def write_logs(message, path, announce):
    # Filter value
    # for _, datas in message.items():
    data = message
    with open(path, 'a') as file:
        # for data in datas:
        value = data.value.decode('utf-8')
        value = json.loads(value)
        file.write(f'{value} - {datetime.now()} - {announce}')

def example(topic):
    prod_tasks = [
        Producer(topic=topic),
    ]
    
    cons_tasks = [
        Consumer(topic=topic, group_id='nhom-01' ,announce='writed from Consumer-01 Group-id-01-01\n', path='./logs/log01.txt', function=write_logs),
        Consumer(topic=topic, group_id='nhom-02', announce='writed from Consumer-02 Group-id-02-01\n', path='./logs/log02.txt', function=write_logs),
        Consumer(topic=topic, group_id='nhom-02', announce='writed from Consumer-02 Group-id-02-02\n', path='./logs/log02.txt', function=write_logs)
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

    # for task in prod_tasks:
    #     task.join()
    for task in cons_tasks:
        task.join()
    
    print("Thread of Consumber has stopped.")
    
    
if __name__=='__main__':
    # topic and producer
    topic_name='demo-03'
    
    # run main
    example(topic_name)