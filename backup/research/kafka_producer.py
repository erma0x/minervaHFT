import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
              api_version=(0,11,5),
              value_serializer=lambda x: dumps(x).encode('utf-8'))
              
for _ in range(100):
    producer.send('foobar', b'some_message_bytes')
    time.sleep(0.4)