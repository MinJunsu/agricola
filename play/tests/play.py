from play.tests.base import BaseTestCase


class PlayTestCase(BaseTestCase):
    """
    플레이어 게임 턴 변경 테스트
    """

    async def test_unittest_turn(self):
        # GIVEN: 사용자가 사용할 커맨드
        turn = 0
        command = {
            "command": "action",
            "player": turn,
            "card_number": "BASE_01"
        }

        # WHEN: 사용자가 특정한 행동 칸 플레이를 진행하였다.
        after = self.game.play(command)

        # THEN: 결과 값의 플레이가 1 증가하였다.
        self.assertEqual(after.get("turn"), turn + 1)

    """
    BASE_01 카드 작동 테스트
    BASE_01: wood 자원이 1 증가한다.
    """

    async def test_moduletest_base_card_works(self):
        # GIVEN: 사용자가 사용할 커맨드
        prev = self.game.to_dict()
        turn = 0
        command = {
            "command": "action",
            "player": turn,
            "card_number": "BASE_01"
        }
        prev_resource = dict(**prev.get("players")[turn].get("resource")).get("wood")

        # WHEN: 사용자가 특정한 행동 칸 플레이를 진행하였다.
        after = self.game.play(command)
        after_resource = dict(**after.get("players")[turn].get("resource")).get("wood")

        # THEN: 사용자가 BASE_01 행동을 실행하여 알맞게 자원이 변경되었다.
        self.assertEqual(prev_resource + 1, after_resource)
