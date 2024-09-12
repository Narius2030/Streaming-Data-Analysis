from functions.KafkaComponent import Consumer
import time
import json
from datetime import datetime


def write_logs(message, path, bonus):
    # Filter value
    for _, datas in message.items():
        # print(datas)
        with open(path, 'w') as file:
            for data in datas: 
                value = data.value.decode('utf-8')
                value = json.loads(value)
                file.write(f'{value} - {datetime.now()} - {bonus}')

def example(topic):
    tasks = [
        Consumer(topic=topic, group_id='nhom-01' ,bonus='writed from Consumer-01 Group-id-01-01\n', path='./logs/log01.txt', cond=write_logs),
        Consumer(topic=topic, group_id='nhom-02', bonus='writed from Consumer-02 Group-id-02-01\n', path='./logs/log02.txt', cond=write_logs)
    ]

    # Start threads of a publisher/producer and a subscriber/consumer to 'my-topic' Kafka topic
    for t in tasks:
        t.start()

    time.sleep(20)

    # Stop threads
    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()
    
    print("Thread of Consumber has stopped.")
    
    
if __name__=='__main__':
    # topic and producer
    topic_name='demo-02'
    
    # run main
    example(topic_name)