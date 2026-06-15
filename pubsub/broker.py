from topic import Topic
from subscriber import Subscriber
from subscription import Subscription
from message import Message
from concurrent.futures import ThreadPoolExecutor
from overflow_policy import OverflowPolicy


class Broker:

    def __init__(self) -> None:
        self._name_to_topic: dict[str, Topic] = {}
        self._pool = ThreadPoolExecutor(max_workers=4)

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
        topic.fan_out(message, self._pool)

    def subscribe(
        self,
        topic_name: str,
        subscriber: Subscriber,
        capacity: int = 1000,
        policy: OverflowPolicy | None = None,
    ) -> Subscription:

        if topic_name not in self._name_to_topic:
            raise ValueError(f"Provided {topic_name} Topic does not exist")

        topic: Topic = self._name_to_topic.get(topic_name)
        subscription = Subscription(
            subscriber=subscriber, topic=topic, capacity=capacity, policy=policy
        )
        topic.add_subscriber(subscription=subscription)

        return subscription

    def unsubscribe(self, topic_name: str, subscription: Subscription) -> Subscription:

        if topic_name not in self._name_to_topic:
            raise ValueError(f"Provided {topic_name} Topic does not exist")

        topic: Topic = self._name_to_topic.get(topic_name)
        topic.remove_subscriber(subscription=subscription)

        return subscription
