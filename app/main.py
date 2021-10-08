from confluent_kafka import Consumer
from confluent_kafka import Producer
import datetime
import time
import json



KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"

def kafka_consumer(group_id:str ) -> int:
    consumer_conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "security.protocol": "plaintext",
        "enable.auto.commit": False,
    }

    consumer = Consumer(consumer_conf)
    return consumer


def consumer_reader():
    topic = "keda-scalling"
    consumer = kafka_consumer(f"{topic}_group")
    consumer.subscribe([topic])

    while True:
        msg = consumer.consume(num_messages=5, timeout=300)
        data = []
        errors = []
        if msg:
            for i in msg:
                if i.error():
                    errors.append(i)
                else:
                    data.append(json.loads(i.value().decode("utf-8")))
            print("data reviced", data)
            # time.sleep(40)

            consumer.commit(asynchronous=False)
        else:
            print("LOL")


if __name__ == "__main__":
    print("running kafka consumer")
    consumer_reader()
