from abc import abstractmethod, ABC
from message import Message


class Subscriber(ABC):

    @abstractmethod
    def on_message(self, message: Message) -> None:
        pass
