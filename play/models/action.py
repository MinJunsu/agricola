from typing import List, Any

from core.const import RESOURCE_CONVERT_FUNCTION, ROOM_UPGRADE_FUNCTION
from core.functions import find_object_or_raise_exception
from core.models import Base
from core.redis import connection
from play.enum import CommandType, FieldType, HouseType
from play.exception import CantUseCardException
from play.models.card import Card
from play.models.field import Field
from play.models.player import Player
from play.models.resource import Resource
from play.models.round_card import RoundCard


class Action(Base):
    redis = connection()

    @classmethod
    def run(
            cls,
            command: CommandType,
            card_number: str,
            players: List[Player],
            round_cards: List[RoundCard],
            turn: int,
            used_round: int,
            common_resource: Resource,
            additional: Any = None,
    ):
        player: Player = players[turn]
        # 데이터 저장을 위해 라운드 카드를 사용한 경우 라운드 카드 변수를 저장한다.
        round_card: RoundCard | None = None
        if "BASE" in card_number or "ACTION" in card_number:
            round_card = find_object_or_raise_exception(round_cards, "card_number", card_number)

            if round_card.get("player") is not None:
                raise CantUseCardException

        card_command = cls.get_command(card_number)

        # 플레이어가 라운드 카드를 선택한 경우 라운드 카드에 플레이어에 대한 정보를 넣어준다.
        if round_card:
            round_card.set("player", turn)

        return eval(card_command)

    # 카드를 낼 때 필요한 자원을 가져간다. -> 필요한 자원을 내는 것 뿐이므로 턴이 유지되는 것은 아님
    @staticmethod
    def require(
            player: Player,
            resource: str,
            amount: int
    ) -> bool:
        if player.get("resource").get(resource) < amount:
            raise Exception("자원이 부족합니다.")
        player.get("resource").set(resource, player.get("resource").get(resource) - amount)
        return True

    # 플레이어에게 행동칸에 존재하는 자원을 추가한다.
    @staticmethod
    def plus(
            player: Player,
            resource: str,
            amount: int
    ) -> bool:
        player.get("resource").set(resource, player.get("resource").get(resource) + amount)
        return True

    # 플레이어가 이동한 행동칸에 존재하는 자원을 제거한다.
    @classmethod
    def use_round_card_resources(
            cls,
            player: Player,
            round_card: RoundCard
    ) -> bool:
        is_dones = []
        for resource, amount in round_card.get("resource").items():
            is_dones.append(cls.plus(player, resource, amount))
            round_card.get("resource")[resource] = 0
        return all(is_dones)

    # 플레이어가 직업 카드를 제출? 선택? 한다.
    @classmethod
    def submit_card(
            cls,
            player: Player,
            round_card: RoundCard,
            used_round: int,
            card_type: str,
            additional: dict,
    ) -> bool:
        # card_type = "JOB" | "SUB | "PRI"
        # Additional Type
        # additional: "JOB_05"
        # 교습
        # BASE_05, BASE_11
        # {
        #     'command': 'additional',
        #     'card_number': 'card_03',
        #     'player': 0,
        #     'additional': {
        #         card_number: str
        #     }
        # }
        card_number = additional.get("card_number")

        if card_type == "JOB":
            # 1. 특정한 직업 카드를 가져온다.
            card: Card = find_object_or_raise_exception(array=player.get("cards"), key="card_number", value=card_number)

            # 2. 플레이어가 현재 몇장의 카드를 가지고 있는지 확인한다.
            card_count = len(list(filter(
                lambda c: "JOB" in c.get("card_number") and c.get("is_use"),
                player.get("cards")
            )))

            # 3. 플레이어가 가지고 있는 카드의 수가 7장 이상이라면 카드를 제출할 수 없다. (예외 처리)
            if card_count > 7:
                raise Exception("더 이상 활성화할 수 있는 직업 카드가 없습니다.")

            # 4. 플레이어가 선택한 행동 칸이 몇개의 자원을 소모하는지 확인한다.
            # BASE_05 -> 2 / BASE_11 -> 1 / card_count 0 -> 0
            cost = 0 if card_count == 0 else 1 if round_card.get('card_number') == 'BASE_11' else 2

            # 5. 플레이어가 직업 카드를 내기 위해 소모되는 자원이 있는지 확인한다. (require)
            cls.require(player=player, resource='food', amount=cost)

            # 6. 플레이어에 선택한 직업 카드의 is_use 속성을 True로 변경하고, 카드 효과를 실행한다.
            return card.use(used_round=used_round, player=player)

        elif card_type == "SUB":
            # 1. 특정한 보조설비 카드를 가져온다.
            card: Card = find_object_or_raise_exception(array=player.get("cards"), key="card_number", value=card_number)

            # 2. 보조설비의 조건을 확인한다.
            card_condition = cls.get_condition(card_number)
            # print(card_condition)
            # print(cls.get_cost(card_number))

            # 3. 플레이어가 조건을 만족하는 지 확인한다.
            # if eval(card_condition):
            #     # 4. 보조설비의 비용을 확인한다.
            #     eval(cls.get_cost(card_number))

            # 5. 플레이어가 보조설비를 내기 위해 소모되는 자원이 있는 지 확인한다. (require)
            # "위에서 처리된다"

            # 6. 플레이어가 선택한 보조 설비 카드의 is_use 속성을 True로 변경하고, 카드 효과를 실행한다.
            return card.use(used_round=used_round, player=player)

        return False

    @classmethod
    def get_command(cls, card_number: str) -> str:
        return cls.redis.hget("commands", card_number)

    @classmethod
    def get_condition(cls, card_number: str) -> str:
        return cls.redis.hget("condition", card_number)

    @classmethod
    def get_cost(cls, card_number: str) -> str:
        return cls.redis.hget("costs", card_number)

    @classmethod
    def convert_resource(
            cls,
            player: Player,
            command: CommandType,
            card_number: str,
            common_resource: Resource,
            additional: dict
    ):
        resources = additional.get("resources")

        # TODO: 플레이어가 card_number에 해당하는 카드를 들고 있는지 확인
        TARGET = "food"
        for resource, count in resources.items():
            ratio = RESOURCE_CONVERT_FUNCTION[card_number][command.value][resource]
            # 1. validate 처리 (플레이어가 자원을 가져갈 수 있는지)
            cls.require(player, resource, count)
            if common_resource.get(TARGET) < count * ratio:
                raise Exception("공용 자원이 부족합니다.")
            # 2. 자원 변경 처리
            cls.plus(player, TARGET, count * ratio)
        return True

    @classmethod
    def increment_family_number(
            cls,
            is_quick: bool,
            player: Player,
            round_card: RoundCard,
            used_round: int,
            additional: str | None = None
    ):
        # Additional Type
        # additional: "JOB_05"

        player_rooms = filter(lambda p: p.get('field_type') == FieldType.ROOM, player.get('fields'))
        # 급한 가족 늘리기가 아니라면
        if not is_quick:
            try:
                # 플레이어 방에서 빈 방을 찾는다.
                empty_room = next(filter(lambda p: p.get('is_in').get('family') == 0, player_rooms))
            except StopIteration:
                raise Exception("플레이어에게 빈 방이 존재하지 않습니다.")

        else:
            try:
                # 플레이어 방에서 빈 방을 찾는다.
                empty_room = next(filter(lambda p: p.get('is_in').get('family') == 0, player_rooms))
            except StopIteration:
                player_rooms = filter(lambda p: p.get('field_type') == FieldType.ROOM, player.get('fields'))
                empty_room = next(player_rooms)

        # 빈 방이 존재한다면 빈 방에 가족 구성원 하나를 추가해준다.
        empty_room.get('is_in').set('family', empty_room.get('is_in').get('family') + 1)
        cls.plus(player, 'family', 1)

        # 만약 급한 가족 늘리기 행동이었다면 보조 설비 카드 추가해주기
        # if not is_quick:
        #     if not additional:
        #         raise Exception('보조 설비 가트를 내주세요.')
        #     cls.submit_card(
        #         player=player, round_card=round_card, card_type='SUB',
        #         used_round=used_round, card_number=additional
        #     )
        return True

    # fileds 중 arrival의 position과 자원을 입력받아 새로 선택한 departures의 position에 옮기는 함수
    # client 입력값 (arrival, departures, count)
    @classmethod
    def move_animal(
            cls,
            player: Player,
            additional: dict,
    ):
        # Additional Type
        # {
        #     'animal': 'sheep',
        #     'count': 1,
        #     'departure': 1,
        #     'arrival': 3
        # }
        fields: List[Field] = player.get("fields")

        # TODO: 예외 처리 추가
        # TODO: 울타리 안에 들어갈 수 있는 최대 동물 수를 초과할 수 없다.

        # 아래 4가지 변수들의 input 값이 정상적인지 확인
        animal: str = additional.get("animal", None)
        count: int = additional.get("count", None)
        departure: int = additional.get("departure", None)
        arrival: int = additional.get("arrival", None)

        if animal is None or count is None or departure is None or arrival is None:
            raise Exception("입력값이 잘못되었습니다.")

        departure_field: Field = find_object_or_raise_exception(array=fields, key="position", value=departure)
        arrival_field: Field = find_object_or_raise_exception(array=fields, key="position", value=arrival)

        # 동물이 아닌 자원을 이동시킬 수는 없다.
        if additional.get("animal") != "sheep" or "boar" or "cattle":
            raise Exception("동물이 아닌 자원을 이동시킬 수는 없습니다.")

        # 출발지와 목적지가 울타리가 아닐 수 없다.
        if player.get("fields")[departure - 1].get("field_type") != FieldType.CAGE or \
                player.get("fields")[arrival - 1].get("field_type") != FieldType.CAGE:
            raise Exception("선택한 농지가 울타리가 아닙니다.")

        if departure_field.get("animal").get(animal) < count:
            raise Exception("출발지에 해당하는 동물이 충분하지 않습니다.")

        departure_field.move(arrival=arrival_field, animal=animal, count=count)

        return False

    """
    밭 일구기
    """

    @classmethod
    def plow_field(
            cls,
            player: Player,
            common_resource: Resource,
            round_card: RoundCard,
            additional: dict
    ):
        # 밭 일구기
        # {
        #     "command": "additional",
        #     "card_number": "ACTION_12",
        #     "player": 0,
        #     "additional": {
        #         "position": 3
        #     }
        # }
        # 씨 뿌리기
        # {
        #     "command": "additional",
        #     "card_number": "ACTION_12",
        #     "player": 0,
        #     "additional": {
        #         "sow_position": 3,
        #         "seed": 'grain'
        #     }
        # }
        # 밭 일구기 & 씨 뿌리기
        # {
        #     "command": "additional",
        #     "card_number": "ACTION_12",
        #     "player": 0,
        #     "additional": {
        #         "position": 3
        #         "sow_position": 3,
        #         "seed": 'grain'
        #     }
        # }
        position = additional.get('position', None)
        sow_position = additional.get("sow_position", None)
        seed = additional.get("seed", None)

        if position is not None:
            # Additional Type
            # additional: position: int
            fields: List[Field] = player.get("fields")

            # field가 이미 존재하는 경우 예외처리
            if fields[position].get("field_type") != FieldType.EMPTY:
                raise Exception("이미 사용중인 농지입니다.")

            # 플레이어 필드에 밭 추가
            fields[position].change_field_type(FieldType.FARM)

        if sow_position is not None:
            cls.sow(
                player=player,
                common_resource=common_resource,
                additional={
                    'sow_position': sow_position,
                    'seed': seed
                }
            )

        return True

    """
    방 만들기
    """

    @classmethod
    def build_room(
            cls,
            player: Player,
            additional: dict,
    ):
        # 농장 확장 카드
        # ACTION_12
        # 만약, 농장 확장 행동칸에서 그리고/또는 행동을 하지 않을 경우
        # {
        #     'command': 'additional',
        #     'card_number': 'ACTION_12',
        #     'additional': {
        #         'positions': [1, 2, 3]
        #     }
        # }
        # 만약 그리고/또는 행동을 할 경우
        # {
        #     'command': 'additional',
        #     'card_number': 'ACTION_12',
        #     'additional': {
        #         'positions': [1, 2, 3],
        #         'barn_position': 3
        #     }
        # }
        positions = additional.get('positions', None)
        barn_position = additional.get("barn_position", None)
        if positions is not None:
            fields: List[Field] = player.get("fields")

            # 방이 이미 최대 개수인 경우 에러처리
            if len(list(filter(lambda x: x.get("field_type") == FieldType.ROOM, fields))) == 5:
                raise Exception("방을 더 이상 만들 수 없습니다.")

            # field가 이미 존재하는 경우 예외처리
            for index in positions:
                if fields[index].get("field_type") != FieldType.EMPTY:
                    raise Exception("이미 사용중인 농지입니다.")

            # TODO: player 트랜잭션 넣어서 자원 수정 처리 require 먼저

            # 플레이어 필드에 방 추가
            for index in positions:
                fields[index].change_field_type(FieldType.ROOM)

        # TODO: 플레이어 필드에 헛간 추가
        if barn_position is not None:
            pass

        return True

    """
    씨 뿌리기
    """

    @classmethod
    def sow(
            cls,
            player: Player,
            common_resource: Resource,
            additional: dict,
    ):
        # 곡식 활용 카드
        # ACTION_01
        # 씨 뿌리기
        # {
        #     'command': 'additional',
        #     'card_number': 'ACTION_12',
        #     'additional': {
        #         'positions': 1,
        #         'seed': 'grain'
        #     }
        # }
        # 빵굽기
        # {
        #     'command': 'additional',
        #     'card_number': 'ACTION_12',
        #     'additional': {
        #         'is_bake': True
        #     }
        # }
        # 씨 뿌리기 & 빵굽기
        # {
        #     'command': 'additional',
        #     'card_number': 'ACTION_12',
        #     'additional': {
        #         'positions': 1,
        #         'seed': 'grain',
        #         'is_bake': True
        #     }
        # }
        position: int = additional.get("position")
        seed: str = additional.get("seed")
        seed_count = 2 if seed == 'grain' else 1
        is_bake: bool = additional.get("is_bake", False)

        if position is not None:
            fields: List[Field] = player.get("fields")

            # field가 밭이 아닌 경우 예외처리
            if fields[position].get("field_type") != FieldType.FARM:
                raise Exception("밭이 아닙니다.")

            # 사용중인 밭인 경우 예외처리
            if fields[position].get("is_in").get("grain") != 0 or fields[position].get("is_in").get("vegetable") != 0:
                raise Exception("이미 사용중인 밭입니다.")

            remain_common_resource = min(common_resource.get(seed), seed_count)
            cls.require(player, seed, 1)
            common_resource.set(seed, common_resource.get(seed) - remain_common_resource)

            # 씨 뿌리기
            if seed == "grain":
                fields[position].add_resource("grain", 1 + remain_common_resource)
            elif seed == "vegetable":
                fields[position].add_resource("vegetable", 1 + remain_common_resource)

        # 빵 굽기
        if is_bake is True:
            print("빵 만들기")
            pass

        return True

    """
    집 고치기
    """

    @classmethod
    def upgrade_house(
            cls,
            player: Player,
            round_card: RoundCard,
            used_round: int,
            additional: dict,
    ):
        # 집 개조
        # ACTION_06
        #
        # {
        #     "command": "action",
        #     "card_number": "ACTION_06",
        #     "player": 0
        # }
        # 집 한 번 고치기 & 주요설비/보조설비
        # {
        #    "command":"additional",
        #    "card_number":"ACTION_06",
        #    "player": 0,
        #    "additional": {
        #        "card_number": "SUB_FAC_01",
        #     }
        # }
        # 집 한 번 고치기 & 울타리 치기
        # {
        #     "command": "additional",
        #     "card_number": "ACTION_02",
        #     "player": 0,
        #     "additional": {
        #         0: [1, 2, 4],
        #         1: [2, 3, 4]
        #     }
        # }
        card_number: str = additional.get("card_number")
        # TODO: 울타리 치기 additional is not None

        house_type = player.get("house_type")
        player_room_count = len(list(filter(lambda f: f.get('field_type') == FieldType.ROOM, player.get('fields'))))

        # 다양한 require 함수를 사용하기 위한 transaction 처리
        player_clone = Player.from_dict(**player.to_dict())

        resources = ROOM_UPGRADE_FUNCTION.get(house_type, None)

        if resources is None:
            raise Exception("이미 최고급 집입니다.")

        for resource, count in resources.items():
            cls.require(player_clone, resource, count * player_room_count)

        player.set('resource', player_clone.get('resource'))

        if house_type == HouseType.WOOD_HOUSE:
            player.set("house_type", HouseType.CLAY_HOUSE)

        elif house_type == HouseType.CLAY_HOUSE:
            player.set("house_type", HouseType.STONE_HOUSE)

        if card_number is not None:
            cls.submit_card(
                player=player,
                round_card=round_card,
                used_round=used_round,
                card_type="SUB",
                additional=additional,
            )

        return True
