from json import dumps
import threading
from datetime import date
from kafka import KafkaProducer, KafkaConsumer


class Producer(threading.Thread):
    def __init__(self, topic, key=None, function=None):
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
                data, key = self.function(page)
                producer.send(self.topic, value={'data': data}, key=f"page_{str(key)}")
            self.stop()
                
        producer.close()
    

class Consumer(threading.Thread):
    def __init__(self, topic, group_id, announce=None, function=None, path=None):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.topic = topic
        self.group_id = group_id
        self.announce = announce
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
            # for message in consumer:
            # Processing Function
            if not message:
                continue
            self.function(message, self.path, self.announce)
            # Termination Event
            if self.stop_event.is_set():
                break
        consumer.close()

    