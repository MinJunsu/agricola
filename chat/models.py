from core.formatter import dict_to_json


class ChatMessage:
    def __init__(self, message, user, timestamp):
        self.message = message
        self.user = user
        self.timestamp = timestamp

    def __str__(self):
        return str(self.__dict__)
