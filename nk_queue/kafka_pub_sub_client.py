import json

from kafka import KafkaClient, KafkaProducer, KafkaConsumer
from retrying import retry

from nk_queue.abstract_pub_sub_client import AbstractPubSubClient


class KafkaPubSubClient(AbstractPubSubClient):
    def __init__(self, kafka_brokers, producer_topics, consumer_topic, group_id):
        self._kafka_brokers = kafka_brokers
        self._producer_topics = producer_topics
        self._consumer_topic = consumer_topic
        self._group_id = group_id
        self._kafka_client = None
        self._producer = None
        self._consumer = None

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10 * 1000,
        stop_max_attempt_number=15,
    )
    def _get_client(self):
        try:
            return KafkaClient(hosts=self._kafka_brokers)
        except Exception as e:
            print(f"Waiting on {self._kafka_brokers} {e}")
            raise e

    def _create_kafka_producer_topics(self):
        for topic in self._producer_topics:
            self._ensure_topic_exists(topic)

    def _ensure_topic_exists(self, topic):
        self._kafka_client.ensure_topic_exists(topic)

    # Only initialize consumer and topic if message requested.
    def _get_kafka_consumer(self):
        if not self._consumer:
            self._ensure_topic_exists(self._consumer_topic)

            self._consumer = KafkaConsumer(
                self._consumer_topic,
                bootstrap_servers=self._kafka_brokers,
                group_id=self._group_id)

        return self._consumer

    def initialize(self):
        self._kafka_client = self._get_client()
        self._create_kafka_producer_topics()
        self._producer = KafkaProducer(bootstrap_servers=self._kafka_brokers)

    def publish(self, message, topic):
        self._producer.send(topic, message.encode("utf-8"))

    def get_message(self):
        return self._get_kafka_consumer()
