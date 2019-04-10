from unittest.mock import MagicMock, Mock
import json
import os
import pytest

from kafka import KafkaClient, KafkaProducer, KafkaConsumer

from nk_queue.kafka_pub_sub_client import KafkaPubSubClient

KAFKA_BROKERS = os.getenv("KAFKA_BROKERS")
LOCAL_TEST_RUN = os.getenv("LOCAL_TEST_RUN", 0)


@pytest.mark.skipif(LOCAL_TEST_RUN == 0, reason="Kafka tests only run locally, no docker image setup yet.")
@pytest.mark.order1
def test_initialize():
    client = KafkaPubSubClient(KAFKA_BROKERS, ["producer.topic.test"], "producer.topic.test", "test_group_id")
    mock_client = KafkaClient(hosts=KAFKA_BROKERS)
    mock_client.ensure_topic_exists = MagicMock()

    client._get_client = MagicMock(return_value=mock_client)

    client.initialize()

    assert mock_client.ensure_topic_exists.call_count == 2
    assert isinstance(client._producer, KafkaProducer)
    assert isinstance(client._consumer, KafkaConsumer)


@pytest.mark.skipif(LOCAL_TEST_RUN == 0, reason="Kafka tests only run locally, no docker image setup yet.")
@pytest.mark.order2
def test_publish():
    client = KafkaPubSubClient(KAFKA_BROKERS, ["producer.topic.test"], "producer.topic.test", "test_group_id")
    client.initialize()
    client.publish(json.dumps({"message": "test message"}), "producer.topic.test")
    assert True


@pytest.mark.skipif(LOCAL_TEST_RUN == 0, reason="Kafka tests only run locally, no docker image setup yet.")
@pytest.mark.order3
def test_get_message():
    client = KafkaPubSubClient(KAFKA_BROKERS, ["producer.topic.test"], "producer.topic.test", "test_group_id")
    client.initialize()

    decoded_message = ""
    for message in client.get_message():
        decoded_message = json.loads(message.value.decode("utf-8"))
        break

    assert decoded_message == {"message": "test message"}
