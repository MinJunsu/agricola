import json
from typing import TypeVar, List, Any


def json_to_dict(data) -> dict:
    return dict(json.loads(data.decode('utf-8')))


def dict_to_json(data: dict):
    return json.dumps(data, ensure_ascii=False).encode('utf-8')


T = TypeVar('T')


def find_object_or_raise_exception(array: List, key: str, value: Any) -> T:
    try:
        return next(filter(lambda x: x.get(key) == value, array))
    except StopIteration:
        raise Exception(f"{key} does not exist")
