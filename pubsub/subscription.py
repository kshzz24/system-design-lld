from __future__ import annotations
from typing import TYPE_CHECKING

from subscriber import Subscriber
import queue
from message import Message
from concurrent.futures import ThreadPoolExecutor
import threading

if TYPE_CHECKING:
    from topic import Topic

BATCH_SIZE = 10


class Subscription:
    _subscriber: Subscriber
    _topic: Topic

    def __init__(self, subscriber: Subscriber, topic: Topic) -> None:
        self._subscriber = subscriber
        self._topic = topic
        self._claim = threading.Lock()
        self._queue: queue.Queue = queue.Queue()

    def enqueue(self, message: Message) -> None:
        self._queue.put(message)

    def try_dispatch(self, pool: ThreadPoolExecutor) -> None:
        if self._claim.acquire(blocking=False):
            pool.submit(self._drain_batch, pool)

    def _drain_batch(self, pool: ThreadPoolExecutor) -> None:
        try:
            for _ in range(BATCH_SIZE):
                try:
                    message = self._queue.get_nowait()
                except queue.Empty:
                    break

                try:
                    self._subscriber.on_message(message)
                except Exception as e:
                    print(f"Error {e} has occurred")
        finally:
            self._claim.release()

        if not self._queue.empty() and self._claim.acquire(blocking=False):
            pool.submit(self._drain_batch, pool)
