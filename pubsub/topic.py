from __future__ import annotations
from typing import TYPE_CHECKING
from message import Message

if TYPE_CHECKING:
    from subscription import Subscription


class Topic:
    def __init__(self, name: str):
        self._name = name
        self._subscriptions: list[Subscription] = []

    def add_subscriber(self, subscription: Subscription) -> None:
        self._subscriptions.append(subscription)

    def remove_subscriber(self, subscription: Subscription) -> bool:
        if subscription in self._subscriptions:
            self._subscriptions.remove(subscription)
            return True
        return False

    def fan_out(self, message: Message) -> None:
        for subscription in self._subscriptions:
            subscription.subscriber.on_message(message)
