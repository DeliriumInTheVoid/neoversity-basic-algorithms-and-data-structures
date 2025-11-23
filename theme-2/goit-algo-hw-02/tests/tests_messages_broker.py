import time
from sources.messages_broker import Message, MessageBroker

class DummyLogger:
    def __init__(self):
        self.logs = []
    def info(self, msg):
        self.logs.append(msg)

def test_broker_start_stop(monkeypatch):
    broker = MessageBroker()

    broker._MessageBroker__logger = DummyLogger()

    def fast_generate_request():
        for _ in range(2):
            msg = Message("quick test")
            broker._MessageBroker__request_queue.put(msg)
            time.sleep(0.01)
    def fast_process_request():
        for _ in range(2):
            try:
                msg = broker._MessageBroker__request_queue.get(timeout=0.1)
                if msg is None:
                    break
            except Exception:
                break
    broker._MessageBroker__generate_request = fast_generate_request
    broker._MessageBroker__process_request = fast_process_request
    broker.start()
    time.sleep(0.05)
    broker.stop()
    assert not broker._MessageBroker__is_running


def test_message_broker_queue_behavior():
    broker = MessageBroker()
    broker._MessageBroker__logger = DummyLogger()

    msg1 = Message("msg1")
    msg2 = Message("msg2")
    broker._MessageBroker__request_queue.put(msg1)
    broker._MessageBroker__request_queue.put(msg2)
    assert broker._MessageBroker__request_queue.get() == msg1
    assert broker._MessageBroker__request_queue.get() == msg2
