import queue
import threading
from dataclasses import dataclass, field
from typing import Any
import time


@dataclass
class Message:
    topic: str
    payload: Any
    timestamp: float = field(default_factory=time.time)


class Broker:
    def __init__(self):
        self._subscriptions: dict[str, list[queue.Queue]] = {}
        self._lock = threading.Lock()
        self._inbox = queue.Queue[Message | None] = queue.Queue()
        self._thread = threading.Thread(target=self._dispatch_loop, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._inbox.put(None)
        self._thread.join()

    def subscribe(self, topic: str, q: queue.Queue) -> None:
        with self._lock:
            self._subscriptions.setdefault(topic, []).append(q)

    def unsubscribe(self, topic: str, q: queue.Queue) -> None:
        with self._lock:
            subscriptions = self._subscriptions.get(topic, [])

            if q in subscriptions:
                subscriptions.remove(q)

    def publish(self, message: Message) -> None:
        self._inbox.put(message)

    def dispatch_loop(self):
        while True:
            message = self._inbox.get()

            if message is None:
                break

            with self._lock:
                subscribers = list(self._subscriptions.get(message.topic, []))

                for q in subscribers:
                    try:
                        q.put_nowait(message)
                    except queue.Full:
                        print("Queue is full, droping message")
                        pass
