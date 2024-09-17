from json import dumps
import threading
from datetime import date
from kafka import KafkaProducer, KafkaConsumer


class Producer(threading.Thread):
    def __init__(self, topic:str, key:str=None, function=None):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.topic = topic
        self.key = key
        self.function = function

    def stop(self):
        self.stop_event.set()
        
    def run(self):
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                 key_serializer=str.encode,
                                 value_serializer=lambda x: dumps(x).encode('utf-8'))
        # send data to topic
        while not self.stop_event.is_set():
            for page in range(1,6):
                data = self.function(page)
                producer.send(self.topic, value={'data':data, 'type':str(self.key), 'page':page}, key=f"{str(self.key)}")
            self.stop()
                
        producer.close()
    

class Consumer(threading.Thread):
    def __init__(self, topic:str, group_id:str=None, announce:str=None, 
                 path:str=None, function=None):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.topic = topic
        self.group_id = group_id
        self.path = path
        self.function = function

    def stop(self):
        self.stop_event.set()
        
    def run(self):
        consumer = KafkaConsumer(self.topic, 
                                 bootstrap_servers=['localhost:9092'],
                                 auto_offset_reset='latest',
                                 auto_commit_interval_ms=2500,
                                 group_id=self.group_id)
        consumer.subscribe([self.topic])
        
        while not self.stop_event.is_set():
            # while True:
            message = consumer.poll(timeout_ms=1000)
            # Processing Function
            if not message:
                continue
            self.function(message, self.path)
            # Termination Event
            if self.stop_event.is_set():
                break
        consumer.close()

    