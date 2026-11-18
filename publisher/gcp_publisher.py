# pip install --upgrade google-cloud-storage

from google.cloud import pubsub_v1
import json

from publisher.config import topic_path
from publisher.publisher_thread import PublishThread
from publisher.singleton import SingletonMeta


class GcpPublisher(PublishThread, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()
        self.publisher = pubsub_v1.PublisherClient()

    def publish_message(self):
        while True:
            message = self.data_queue.get() # wait for data
            message = json.dumps(message).encode("utf-8")
            future = self.publisher.publish(topic_path, message)
            print(f"Published message id : {future.result()}")

    def add_message_to_queue(self, data):
        self.data_queue.put(data)
