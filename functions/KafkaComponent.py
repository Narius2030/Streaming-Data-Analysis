from json import dumps
import threading
import time
from kafka import KafkaProducer, KafkaConsumer


class Producer(threading.Thread):
    def __init__(self, topic):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.topic = topic

    def stop(self):
        self.stop_event.set()
        
    def run(self):
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                value_serializer=lambda x: dumps(x).encode('utf-8'),
                                key_serializer=str.encode)
        # send data to topic
        while not self.stop_event.is_set():
            for num in range(0, 100):
                if num%2 == 0:
                    producer.send(self.topic, value={'number': num}, key='apple')
                else:
                    producer.send(self.topic, value={'number': num}, key='orange')
        producer.close()
    

class Consumer(threading.Thread):
    def __init__(self, topic, group_id, path, bonus=None):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.topic = topic
        self.group_id = group_id
        self.bonus = bonus
        self.path = path

    def stop(self):
        self.stop_event.set()
        
    def run(self):
        consumer = KafkaConsumer(self.topic, bootstrap_servers=['localhost:9092'],
                                auto_offset_reset='latest',
                                group_id=self.group_id)
        consumer.subscribe([self.topic])
        
        while not self.stop_event.is_set():
            with open(self.path, 'w') as file:
                for message in consumer:
                    file.write(f'{message} - {self.bonus}')
                    if self.stop_event.is_set():
                        break
        consumer.close()


def example(topic):
    tasks = [
        Producer(topic=topic),
        Consumer(topic=topic, group_id='nhom-01' ,bonus='writed from Consumer-01\n', path='./logs/log01.txt'),
        Consumer(topic=topic, group_id='nhom-01', bonus='writed from Consumer-02\n', path='./logs/log02.txt')
    ]

    # Start threads of a publisher/producer and a subscriber/consumer to 'my-topic' Kafka topic
    for t in tasks:
        t.start()

    time.sleep(0.5)

    # Stop threads
    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()
    
    print("Thread has stopped.")


if __name__=='__main__':
    # topic and producer
    topic_name='demo-01'
    
    # run main
    example(topic_name)
    