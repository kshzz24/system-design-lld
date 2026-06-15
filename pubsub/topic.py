from __future__ import annotations
from typing import TYPE_CHECKING
from message import Message
import threading

if TYPE_CHECKING:
    from subscription import Subscription


class Topic:
    def __init__(self, name: str):
        self._name = name
        self._subscriptions: list[Subscription] = []
        self._lock = threading.Lock()

    def add_subscriber(self, subscription: Subscription) -> None:
        with self._lock:
            self._subscriptions.append(subscription)

    def remove_subscriber(self, subscription: Subscription) -> bool:
        with self._lock:
            if subscription in self._subscriptions:
                self._subscriptions.remove(subscription)
                return True
            return False

    def fan_out(self, message: Message, pool) -> None:

        with self._lock:
            snapshot = list(self._subscriptions)
        for subscription in snapshot:
            subscription.enqueue(message)
            subscription.try_dispatch(pool)
