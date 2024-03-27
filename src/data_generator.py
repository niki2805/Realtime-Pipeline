import json
import socket
import threading
import time

from confluent_kafka import Producer

from eventschema import Category, Event
from faker import Faker

conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()}

producer = Producer(conf)
fake = Faker()


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


def send_to_kafka(topic: str, data: str):
    producer.produce(topic, value=data, callback=acked)


def each_event(category_name: str, event: Event):
    n = 5 * 60 * 1000 // event.number
    while n:
        data = fake.get_fake_event(event.event_name, event.required_attributes)
        print(n)
        send_to_kafka(category_name, json.dumps(data))
        n -= 1
        time.sleep(event.number / 1000)


def each_category(category: Category):
    for event in category.events:
        thread = threading.Thread(target=each_event, args=(category.category_name, event),
                                  name="thread-event-" + event.event_name)
        thread.start()


def main():
    with open("resources/events_schema.json") as fp:
        events_schema = json.load(fp)
        for datum in events_schema:
            category = Category.from_dict(datum)
            thread = threading.Thread(target=each_category, args=(category,), name="thread-" + category.category_name)
            thread.start()


if __name__ == '__main__':
    main()
