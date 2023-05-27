import json


def json_to_dict(data) -> dict:
    return dict(json.loads(data.decode('utf-8')))


def dict_to_json(data: dict):
    return json.dumps(data, ensure_ascii=False).encode('utf-8')
