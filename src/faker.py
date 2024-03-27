import datetime
import json
import random


class Faker:
    def __init__(self):
        self.strings = {}
        with open("resources/genres.json") as f:
            self.strings["genre"] = json.load(f)
        with open("resources/terms.json") as f:
            self.strings["term"] = json.load(f)

        self.current_timestamp = datetime.datetime(2022, 12, 1, 12, 00, 00)

    def _get_fake_data(self, data_type):
        if data_type.startswith("string"):
            key = data_type[7:]
            return random.choice(self.strings[key])
        elif data_type.startswith("int"):
            a, b = data_type[4:].split()
            return random.randint(int(a), int(b))
        elif data_type == "ip":
            return "192.168.0." + str(random.randint(0, 10))
        elif data_type == "datetime":
            timestamp = self.current_timestamp + datetime.timedelta(minutes=random.randrange(60),
                                                                    seconds=random.randrange(60))
            return str(timestamp)
        else:
            raise Exception("Unknown data_type: " + data_type)

    def get_fake_event(self, event_name, attributes):
        attrs = {}
        for attribute in attributes:
            attrs[attribute.name] = self._get_fake_data(attribute.data_type)

        return {
            "event_name": event_name,
            "attributes": attrs
        }
