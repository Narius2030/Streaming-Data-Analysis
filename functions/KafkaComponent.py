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
                                value_serializer=lambda x: dumps(x).encode('utf-8'))
        # send data to topic
        num = 0
        while not self.stop_event.is_set():
            num += 1
            if num%2 == 0:
                producer.send(self.topic, value={'number': num}, partition=0)
            else:
                producer.send(self.topic, value={'number': num}, partition=1)
                
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
        consumer = KafkaConsumer(self.topic, bootstrap_servers=['localhost:9092'],
                                auto_offset_reset='latest',
                                group_id=self.group_id)
        consumer.subscribe([self.topic])
        
        while not self.stop_event.is_set():
            # while True:
            #     message = consumer.poll(timeout_ms=1000)
            with open(self.path, 'a') as file:
                file.write(f'========================================== {date.today()} ==========================================\n\n')
            for message in consumer:
                # Processing Function
                if not message:
                    continue
                self.function(message, self.path, self.announce)
                # Termination Event
                if self.stop_event.is_set():
                    break
        consumer.close()

    