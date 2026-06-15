from dataclasses import dataclass, field
from topic import Topic
from subscriber import Subscriber
from subscription import Subscription
from message import Message


@dataclass
class Broker:
    _name_to_topic: dict[str, Topic] = field(default_factory=dict)

    def create_topic(self, topic_name: str) -> Topic:
        if topic_name in self._name_to_topic:
            raise ValueError("Topic already exists")

        topic = Topic(name=topic_name)
        self._name_to_topic[topic_name] = topic
        return topic

    def publish(self, topic_name: str, message: Message) -> None:
        if topic_name not in self._name_to_topic:
            raise ValueError(f"Provided {topic_name} Topic does not exist")

        topic: Topic = self._name_to_topic.get(topic_name)
        topic.fan_out(message)

    def subscribe(self, topic_name: str, subscriber: Subscriber) -> Subscription:

        if topic_name not in self._name_to_topic:
            raise ValueError(f"Provided {topic_name} Topic does not exist")

        topic: Topic = self._name_to_topic.get(topic_name)
        subscription = Subscription(subscriber=subscriber, topic=topic)
        topic.add_subscriber(subscription=subscription)

        return subscription

    def unsubscribe(self, topic_name: str, subscription: Subscription) -> Subscription:

        if topic_name not in self._name_to_topic:
            raise ValueError(f"Provided {topic_name} Topic does not exist")

        topic: Topic = self._name_to_topic.get(topic_name)

        topic.remove_subscriber(subscription=subscription)

        return subscription
