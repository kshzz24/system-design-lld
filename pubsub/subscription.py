from __future__ import annotations
from typing import TYPE_CHECKING

from subscriber import Subscriber
import queue
import threading
from message import Message

if TYPE_CHECKING:
    from topic import Topic

_SHUTDOWN = object()


class Subscription:
    _subscriber: Subscriber
    _topic: Topic

    def __init__(self, subscriber: Subscriber, topic: Topic) -> None:
        self._subscriber = subscriber
        self._topic = topic
        self._queue: queue.Queue = queue.Queue()
        self._worker = threading.Thread(target=self._drain, daemon=True)
        self._worker.start()

    def enqueue(self, message: Message) -> None:
        self._queue.put(message)

    def _drain(self):
        while True:
            message = self._queue.get()
            if message is _SHUTDOWN:
                break
            try:
                self._subscriber.on_message(message)
            except Exception as e:
                print(f"Error {e} has occurred")

    def close(self) -> None:
        self._queue.put(_SHUTDOWN)
