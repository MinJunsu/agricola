from typing import List

from core.const import RESOURCE_CONVERT_FUNCTION
from core.models import Base
from core.redis import connection
from play.models.player import Player
from play.models.player import RoundCard

class Action(Base):
    redis = connection()

    def run(self, players: List[Player], round_card):
        redis = connection()
        player = players[self._turn]
        self._player = player
        self._players = players
        command = redis.hget("commands", self._card_number)
        self.use_round_card_resources(round_card)
        print(self._player)
        print(round_card)
        is_done = all(eval(command))
        return is_done

    # 카드를 낼 때 필요한 자원을 가져간다. -> 필요한 자원을 내는 것 뿐이므로 턴이 유지되는 것은 아님
    def require(self, player, resource: str, amount: int) -> bool:
        if player.get("resources").get(resource) < amount:
            raise Exception("자원이 부족합니다.")
        player.get("resources").set(resource, player.get("resources").get(resource) - amount)
        return True

    # 플레이어에게 행동칸에 존재하는 자원을 추가한다.
    def plus(self, player, resource: str, amount: int) -> bool:
        player.get("resource").set(resource, player.get("resource").get(resource) + amount)
        return True

    # 플레이어가 이동한 행동칸에 존재하는 자원을 제거한다.
    @staticmethod
    def use_round_card_resources(self, round_card):
        for resource, amount in round_card.get("resource").items():
            self.plus(self._player, resource, amount)
            round_card.get("resource")[resource] = 0
        return True

    @classmethod
    def convert_resource(
            cls,
            player: Player,
            command: str,
            card_number: str,
            resources: dict
    ):
        redis = cls.redis
        TARGET = "food"
        player_resources = player.get("resources")
        for resource, count in resources.items():
            ratio = RESOURCE_CONVERT_FUNCTION[card_number][command][resource]
            player_resources.set(resource, player_resources.get(resource) + resources[resource])
            player_resources.set(TARGET, player_resources.get(TARGET) + resources[resource])
            # TODO: 1. validate 처리 (플레이어가 자원을 가져갈 수 있는지)
            # TODO: 2 자원 변경 처리
    
    # 플레이어가 직업 카드를 제출? 선택? 한다.
    @classmethod
    def job_submit_card(
            cls,
            player: Player,
            round_card: RoundCard,
            card_number: str
    ) -> bool:
        # 1. 플레이어가 현재 몇장의 카드를 가지고 있는지 확인한다.
        card_count = len(filter(
            lambda card: "JOB" in card.get("card_number") and card.get("is_use") == True,
            player.get("cards")
        ))
        # 2. 플레이어가 가지고 있는 카드의 수가 7장 이상이라면 카드를 제출할 수 없다. (예외 처리)
        if(card_count>7):
            raise Exception("더 이상 활성화할 수 있는 직업 카드가 없습니다.")
        # 3. 플레이어가 선택한 행동 칸이 몇개의 자원을 소모하는지 확인한다.
        
        
        #카드 0개면 그냥 활성화하고 리턴
        if card_count == 0:
            
            pass
        
        
        cost = 2
        if round_card.card_number == 'BASE_05':
            cost = 1
        # 4. 플레이어가 직업 카드를 내기 위해 소모되는 자원이 있는지 확인한다. (require)
        cls.require(player=player, resource='food', amount=cost)
        # 5. 플레이어에 선택한 직업 카드의 is_use 속성을 True로 변경한다.
        return True
    
    @classmethod
    def fac_submit_card(
            cls,
            player: Player,
            round_card: RoundCard
    ) -> bool:
        # 1. 플레이어가 현재 몇장의 카드를 가지고 있는지 확인한다.
        
        # 2. 플레이어가 가지고 있는 카드의 수가 7장 이상이라면 카드를 제출할 수 없다. (예외 처리)

        # 3. 플레이어가 선택한 행동 칸이 몇개의 자원을 소모하는지 확인한다.
        
        # 4. 플레이어가 직업 혹은 보조설비 카드를 내기 위해 소모되는 자원이 있는지 확인한다. (require)
        # 5. 플레이어에 선택한 직업 카드의 is_use 속성을 True로 변경한다.
        return True