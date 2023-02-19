from pykafka import KafkaClient
import pickle
import json
client = KafkaClient(hosts="localhost:9092")

topic = client.topics['orderbook']

consumer = topic.get_simple_consumer()

# Iterate through messages in the topic
for message in consumer:
    if message is not None:
        #
        print(message.value)
        message
        #data = json.loads(message.value)
        #print('-'*80)
        #print(data)