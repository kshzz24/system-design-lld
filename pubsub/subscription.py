from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass
from subscriber import Subscriber

if TYPE_CHECKING:
    from topic import Topic


@dataclass
class Subscription:
    subscriber: Subscriber
    topic: Topic
