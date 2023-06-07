from play.models.action import Action
from play.tests.base import BaseTestCase


class ActionTestCase(BaseTestCase):
    """
    플레이어 자원 증가 테스트
    """
    """
    plus 테스트
    Player의 자원을 증가시킨다.
    """

    async def test_unittest_resource_increase(self):
        # GIVEN: 입력값
        player = self.game.get("players")[0]
        resource = "sheep"
        amount = 4

        # WHEN: 사용자의 자원을 증가시킨다.
        prev_resource = player.get("resource").get(resource)
        Action.plus(player, resource, amount)

        # THEN: 사용자의 자원이 증가하였다.
        self.assertEqual(prev_resource + 4, player.get("resource").get(resource))

    """
    require 테스트
    Player의 자원을 감소시킨다.
    """

    async def test_unittest_resource_decrease(self):
        # GIVEN: 입력값
        player = self.game.get("players")[0]
        resource = "sheep"
        amount = 4

        player.get("resource").set(resource, 4)  # 사용자에게 임시로 자원을 부여한다.

        # WHEN: 사용자의 자원을 감소시킨다.
        prev_resource = player.get("resource").get(resource)
        Action.require(player, resource, amount)

        # THEN: 사용자의 자원이 감소하였다.
        self.assertEqual(prev_resource - 4, player.get("resource").get(resource))

    """
    use_round_card_resource 테스트
    행동칸에 존재하는 자원을 제거한다.
    """

    async def test_unittest_use_round_card_resource(self):
        # GIVEN: 입력값
        player = self.game.get("players")[0]
        round_card = self.game.get("round_cards")[0]

        # round_card에 임시로 자원을 부여한다.
        round_card.get("resource").set("sheep", 4)

        # WHEN: round_card에 자원을 감소시킨다.
        prev_resource = round_card.get("resource").get("sheep")
        Action.use_round_card_resources(player, round_card)

        # THEN: round_card에 자원이 감소하였다.
        after_resource = round_card.get("resource").get("sheep")
        self.assertEqual(prev_resource - 4, after_resource)

    """
    submit_card 테스트
    플레이어의 카드를 제출한다.
    """

    async def test_unittest_submit_card(self):
        # GIVEN: 입력값
        player = self.game.get("players")[0]
        round_card = self.game.get("round_cards")[0]
        card_type = "JOB"
        card_number = round_card.get("JOB_05")

        print(round_card)

        # WHEN: 플레이어가 카드를 제출한다.
        Action.submit_card(player, card_type, card_number)

        # THEN: 플레이어의 카드가 제출되었다.
        self.assertEqual(player.get("cards")[0].get("card_number"), card_number)
