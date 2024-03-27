from typing import List
from typing import Any
from dataclasses import dataclass


@dataclass
class RequiredAttribute:
    name: str
    data_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'RequiredAttribute':
        _name = str(obj.get("name"))
        _data_type = str(obj.get("data_type"))
        return RequiredAttribute(_name, _data_type)


@dataclass
class Event:
    event_name: str
    required_attributes: List[RequiredAttribute]
    number: int

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        _event_name = str(obj.get("event_name"))

        _required_attributes = []
        if obj.get("required_attributes"):
            _required_attributes = [RequiredAttribute.from_dict(y) for y in obj.get("required_attributes")]

        _number = 10000
        if obj.get("number"):
            _number = obj.get("number")

        return Event(_event_name, _required_attributes, _number)


@dataclass
class Category:
    category_name: str
    required_attributes: List[RequiredAttribute]
    events: List[Event]

    @staticmethod
    def from_dict(obj: Any) -> 'Category':
        _category_name = str(obj.get("category_name"))
        if obj.get("required_attributes"):
            _required_attributes = [RequiredAttribute.from_dict(y) for y in obj.get("required_attributes")]
        else:
            _required_attributes = []

        _events = []
        for y in obj.get("events"):
            _e = Event.from_dict(y)
            _e.required_attributes += _required_attributes
            _events.append(_e)

        return Category(_category_name, _required_attributes, _events)
