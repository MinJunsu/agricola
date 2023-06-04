from core.const import RESOURCE_CONVERT_FUNCTION
from play.models.player import Player


class Formatter:
    # {
    #     "command": "convert",
    #     "convert": {
    #         "resource": {
    #             "grain": 2,
    #             "sheep": 3,
    #         }
    #     }
    # }
    @staticmethod
    def convert_resource(
            player: Player,
            command: str,
            card_number: str,
            resources: dict
    ):
        TARGET = "food"
        player_resources = player.get("resources")
        for resource, count in resources.items():
            ratio = RESOURCE_CONVERT_FUNCTION[card_number][command][resource]
            player_resources.set(resource, player_resources.get(resource) + resources[resource])
            player_resources.set(TARGET, player_resources.get(TARGET) + resources[resource])
            # TODO: 1. validate 처리 (플레이어가 자원을 가져갈 수 있는지)
            # TODO: 2 자원 변경 처리

    # {
    #     "command": "move",
    #     "move": {
    #         'to': {
    #             'position': 'index',
    #             'resource_name': 'sheep',
    #             'count': 2,
    #         },
    #         'from': {
    #             'position': 'index',
    #             'resource_name': 'sheep',
    #             'count': 2,
    #         }
    #     }
    # }
    @staticmethod
    def move_animal(
            player: Player,
            command: str,
    ):
        pass
