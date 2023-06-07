from core.models import Base


class Card(Base):
    _card_number: str
    _name: str
    _score: int
    _is_used: bool
    _used_round: int
    _is_done = bool

    def __init__(
            self,
            card_number: str,
            name: str,
            score: int,
            used_round: int,
            is_use: bool = False,
            is_done: bool = False
    ):
        self._card_number = card_number
        self._name = name
        self._score = score
        self._is_use = is_use
        self._is_done = True

    # 플레이어가 들고 있는 카드를 사용함과 동시에 라운드 카드에 특정한 이펙트를 추가해준다.
    def use(
            self,
            used_round: int
    ) -> bool:
        self._is_use = True
        self._used_round = used_round
        return True

    def run(
            self,
            player: 'play.models.card.Card',
            card_number
    ):
        # 양의 친구 구현체 self.aa(round=[2, 5, 8, 10], resource={'sheep': 1})
        # 소규모 농부 self.in_round_start(player, 'len(list(filter(lambda p: p.get("field_type") == FieldType.ROOM, player.get("fields")))) == 2', {'wood': 1})

        pass

    # 라운드가 시작 될 경우 간단한 조건(condition)으로 결과를 처리하는 함수
    def in_round_start(
            self,
            player,
            condition: str,
            resources: dict,
    ) -> None:
        if eval(condition):
            for resource, count in resources.items():
                player.get("resource").set(resource, player.get("resource").get(resource) + count)
        return

    # 특정한 행동을 할 경우 실행되는 함수
    @staticmethod
    def in_action(
            player,
            condition: bool,
            resources: dict,
    ) -> None:
        if condition:
            for resource, count in resources.items():
                player.get("resource").set(resource, player.get("resource").get(resource) + count)
        return

    # 조건에 맞는 경우 자원을 가지고 오는 함수
    @staticmethod
    def take_resource_in_condition(
            player,
            condition: str,
            resources: dict,
    ) -> None:
        if eval(condition):
            for resource, count in resources.items():
                player.get("resource").set(resource, player.get("resource").get(resource) + count)
        return

    # 조건에 상관 없이 자원을 가지고 오는 함수
    @staticmethod
    def take_resource(
            player,
            resources: dict
    ):
        for resource, count in resources.items():
            player.get("resource").set(resource, player.get("resource").get(resource) + count)
        return

    # 카드를 내려놓은 즉시 실행할 함수
    def immediately(
            self,
            player,
            condition: str,
            resources: dict
    ) -> None:
        return
