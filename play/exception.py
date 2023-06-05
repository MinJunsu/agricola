class IsNotPlayerTurnException(Exception):
    def __init__(self):
        super().__init__("It's not your turn.")


class CantUseCardException(Exception):
    def __init__(self):
        super().__init__("You can't use this card.")
