import queue
import threading


class PublishThread:
    def __init__(self):
        self.data_queue = queue.Queue()
        self.thread = threading.Thread(target=self.publish_message, daemon=True)
        self.thread.start()

    def publish_message(self):
        pass
