import time
from kafka import TopicPartition,KafkaConsumer
consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
              api_version=(0,11,5))
consumer.assign([TopicPartition('foobar', 2)])
msg = next(consumer)
print(msg)