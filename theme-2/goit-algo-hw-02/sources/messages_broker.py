import queue
import random
import time
import threading
import uuid
from faker import Faker
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class Message:
    def __init__(self, content):
        self.id: str = str(uuid.uuid4())
        self.content: str = content
        self.timestamp: float = time.time()


class MessageBroker:
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("MessageBroker")
        self.__request_queue: queue.Queue = queue.Queue()
        self.__is_running: bool = False
        self.__producer_thread: threading.Thread | None = None
        self.__consumer_thread: threading.Thread | None = None


    def start(self):
        if self.__is_running:
            return
        self.__is_running = True
        self.__producer_thread = threading.Thread(target=self.__generate_request)
        self.__consumer_thread = threading.Thread(target=self.__process_request)

        self.__producer_thread.start()
        self.__consumer_thread.start()


    def stop(self):
        if not self.__is_running:
            return
        self.__logger.info("Stopping the message broker...")
        self.__is_running = False

        if self.__producer_thread:
            self.__producer_thread.join()

        # Signal the consumer to stop by putting a sentinel value in the queue
        self.__request_queue.put(None)

        # wait for the consumer to finish
        if self.__consumer_thread:
            self.__consumer_thread.join()
        self.__logger.info("Message broker stopped.")


    def __generate_request(self):
        """Function to generate new requests and add them to the queue"""

        while self.__is_running:
            message = Message(content=Faker().sentence())
            self.__request_queue.put(message)
            self.__logger.info(f"Message {message.id} added to the queue.")
            time.sleep(random.uniform(0.5, 2)) # time interval between new requests


    def __process_request(self):
        """Function to process requests from the queue"""
        while True: # even if stopped, we want to process remaining items. that's why we use while True not while self.__is_running
            try:
                message = self.__request_queue.get(timeout=1.0)

                if message is None:
                    # Sentinel value received, exit the loop
                    self.__logger.info("Consumer received stop signal. Processing remaining items...")
                    break

                self.__logger.info(f"Processing message {message.id}...")
                time.sleep(random.uniform(1, 3)) # time taken to process the message
                self.__logger.info(f"Message {message.id} processed. Time in queue: {time.time() - message.timestamp:.2f} seconds.")
                self.__logger.info(f"Messages left in queue: {self.__request_queue.qsize()}")
            except queue.Empty:
                if not self.__is_running:
                    break
                continue
