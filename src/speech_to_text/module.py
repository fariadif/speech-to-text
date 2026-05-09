import queue
import threading

from .broker import Broker, Message


class Module:
    def __init__(self, name: str, broker: Broker):
        self.name = name
        self._broker = broker
        self._inbox: queue.Queue[Message | None] = queue.Queue(maxsize=1000)
        self._thread = threading.Thread(target=self._run, name=name, daemon=True)
        self._stop_event = threading.Event()

    def subscribe(self, *topics: str):
        for topic in topics:
            self._broker.subscribe(topic, self._inbox)

    def publish(self, topic: str, payload) -> None:
        self._broker.publish(Message(topic=topic, payload=payload))

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._inbox.put(None)
        self._thread.join()

    def _run(self):
        self.on_start()

        while True:
            msg = self._inbox.get()

            if msg is None:
                break

            self.on_message(msg)

        self.on_stop()

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_message(self, mesg: Message):
        pass
