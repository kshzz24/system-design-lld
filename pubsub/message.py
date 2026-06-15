from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class Message:
    payload: Any
    topic_name: str
    timestamp: datetime
