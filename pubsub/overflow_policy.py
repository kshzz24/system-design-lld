from __future__ import annotations
from abc import ABC, abstractmethod
import queue


class OverflowPolicy(ABC):
    @abstractmethod
    def on_full(self, q: "queue.Queue", message) -> None:
        pass


class DropOldest(OverflowPolicy):
    def on_full(self, q: "queue.Queue", message) -> None:
        try:
            q.get_nowait()  # throw away the OLDEST (front of queue)
        except queue.Empty:
            pass
        try:
            q.put_nowait(message)  # now there's room for the newest
        except queue.Full:
            pass


class DropNewest(OverflowPolicy):
    def on_full(self, q: "queue.Queue", message) -> None:
        #it is empty because in case of full queue we need to skip last message
        pass
