from redis import StrictRedis

_connection = None


def connection() -> StrictRedis:
    global _connection
    if _connection is None:
        _connection = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    return _connection
