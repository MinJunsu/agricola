from typing import List

from core.const import LAST_ROUND
from core.models import Base
from core.redis import connection
from play.models.round_card import RoundCard


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
            used_round: int | None = None,
            is_use: bool = False,
            is_done: bool = False
    ):
        self._card_number = card_number
        self._name = name
        self._score = score
        self._is_use = is_use
        self._is_done = True
        self._used_round = used_round

    # 플레이어가 들고 있는 카드를 사용함과 동시에 라운드 카드에 특정한 이펙트를 추가해준다.
    def use(
            self,
            used_round: int,
            player
    ) -> bool:
        self._is_use = True
        self._used_round = used_round
        redis = connection()
        if "immediately" in redis.hkeys(f'cards:{self._card_number}'):
            command = redis.hget(f'cards:{self._card_number}', 'immediately')
            eval(command)
        return True

    def run(
            self,
            player,
            card_number: str,
            round_cards: List[RoundCard],
            now_round: int
    ):
        redis = connection()
        if "action" in redis.hkeys(f'cards:{self._card_number}'):
            command = redis.hget(f'cards:{self._card_number}', 'action')
            eval(command)
        return None

    # 조건에 맞는 경우 자원을 가지고 오는 함수
    @staticmethod
    def take_resource_in_condition(
            player,
            card_number: str,
            condition: str,
            resources: dict,
    ) -> None:
        if eval(condition):
            for resource, count in resources.items():
                player.get("resource").set(resource, player.get("resource").get(resource) + count)
        return

    @classmethod
    def add_effect_on_round_cards(
            cls,
            turn: int,
            round_cards: List[RoundCard],
            now_round: int,
            resources: dict,
            method: str,
            count: int = 0,
            additional: List = None,
            condition: bool = True
    ) -> None:
        if condition:
            effected_round = cls.calculate_round(
                method=method, now_round=now_round,
                count=count, addtional=additional
            )
            [round_cards[r].add_addtional_action(player_id=turn, resources=resources) for r in effected_round]

        pass

    # 조건에 상관 없이 자원을 가지고 오는 함수
    @staticmethod
    def take_resource(
            player,
            resources: dict
    ):
        for resource, count in resources.items():
            player.get("resource").set(resource, player.get("resource").get(resource) + count)
        return

    # 현재 기준으로 라운드 갯수를 정하는 함수
    @staticmethod
    def calculate_round(
            method: str,
            now_round: int,
            count: int = 0,
            addtional: List = None
    ) -> List:
        # 거대 농장, 하인
        if method == "remain":
            return list(range(now_round + 1, LAST_ROUND + 1))
        # 벽 건축가, 청어 냄비, 도토리 바구니, 딸기포, 연못 오두막
        elif method == "next":
            return list(range(now_round + 1, now_round + count + 1))
        # 대형 온실, 양의 친구
        elif method == "additional":
            return list(set(list(map(lambda x: x + now_round, addtional))) & set(list(range(15))))
        # 손수레
        elif method == "farming":
            return [5, 8, 10, 12, 14]
        # 울창한 숲
        elif method == "even":
            return list(set(list(range(now_round + 1, LAST_ROUND + 1))) & set(list(range(0, 15, 2))))
