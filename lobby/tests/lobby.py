import asyncio

from channels.testing import WebsocketCommunicator
from django.test import TestCase

from agricola.socket_urls import websocket_urlpatterns
from core.redis import connection


class LobbySocketTest(TestCase):
    redis = connection()
    """
    웹 소켓 연결이 정상적으로 이루어지는지 확인한다.
    """

    def setUp(self) -> None:
        asyncio.run(self.connect())

    def tearDown(self) -> None:
        self.redis.flushdb()
        asyncio.run(self.disconnect())

    async def connect(self):
        self.communicator = WebsocketCommunicator(websocket_urlpatterns, "/ws/v1/lobby/")
        await self.communicator.connect()

    async def disconnect(self):
        await self.communicator.disconnect()

    async def test_lobby_connection(self):
        # GIVEN: 웹 소켓 연결
        self.communicator = WebsocketCommunicator(websocket_urlpatterns, "/ws/v1/lobby/")
        await self.communicator.connect()

        # EXPECTED: 정상적으로 연결 되었을 때 데이터 값
        expected = {
            "is_success": True,
            "data": {
                "type": "lobby",
                "result": []
            }
        }

        # WHEN: 연결을 시도하고, 메시지를 받는다.

        response = await self.communicator.receive_json_from()

        # THEN: 연결이 정상적으로 이루어졌는지와, 메시지가 정상적으로 전달되었는지 확인한다.
        self.assertDictEqual(response, expected)

    """
    방을 정상적으로 생성할 수 있는지 확인한다.
    """

    async def test_lobby_create_room(self):
        # GIVEN: 방 생성을 위한 커맨드
        self.communicator = WebsocketCommunicator(websocket_urlpatterns, "/ws/v1/lobby/")
        await self.communicator.connect()
        command = {
            "command": "create",
            "user_id": 1,
            "options": {
                "title": "test_room",
                "password": "test_password",
                "mode": "public",
            }
        }

        response = await self.communicator.receive_json_from()

        # EXPECTED: 정상적으로 방이 생성되었을 때 데이터 값
        expected = {
            "room_id": 1,
            "host": 1,
            "options": {
                "title": "test_room",
                "mode": "public",
                "password": "test_password",
            }
        }

        # WHEN: 방을 생성하고, 메시지를 받는다.
        await self.communicator.send_json_to(command)
        response = await self.communicator.receive_json_from()

        # THEN: 방이 정상적으로 생성되었는지 확인한다.
        self.assertEqual(len(response["data"]["result"]), 1)
        self.assertDictContainsSubset(expected, response["data"]["result"][0])

    """
    방에 입장할 수 있는지 확인한다.
    """

    async def test_lobby_enter_room(self):
        # GIVEN: 입장 가능한 방 생성 커맨드, 방 입장 커맨드
        self.communicator = WebsocketCommunicator(websocket_urlpatterns, "/ws/v1/lobby/")
        await self.communicator.connect()
        user_id_1, user_id_2 = 1, 2
        create_command = {
            "command": "create",
            "user_id": user_id_1,
            "options": {
                "title": "test_room",
                "password": "test_password",
                "mode": "public",
            }
        }
        enter_command = {
            "command": "enter",
            "user_id": user_id_2,
            "room_id": 1,
        }

        # EXPECTED: 정상적으로 방에 입장되었을 때 데이터 값
        expected = [user_id_1, user_id_2]

        # WHEN: 방을 생성하고, 방에 입장하고, 메시지를 받는다.
        await self.communicator.send_json_to(create_command)
        _ = await self.communicator.receive_json_from()

        await self.communicator.send_json_to(enter_command)
        response = await self.communicator.receive_json_from()

        # THEN: 방에 정상적으로 입장되었는지 확인한다.
        self.assertEqual(response['data']['result']['participants'], expected)

    """
    방에서 나갈 수 있는지 확인한다.
    """

    async def test_lobby_exit_room(self):
        # GIVEN: 입장 가능한 방 생성 커맨드, 방 입장 커맨드, 방 퇴장 커맨드
        self.communicator = WebsocketCommunicator(websocket_urlpatterns, "/ws/v1/lobby/")
        await self.communicator.connect()
        user_id_1, user_id_2 = 1, 2
        create_command = {
            "command": "create",
            "user_id": user_id_1,
            "options": {
                "title": "test_room",
                "password": "test_password",
                "mode": "public",
            }
        }
        enter_command = {
            "command": "enter",
            "user_id": user_id_2,
            "room_id": 1,
        }
        exit_command = {
            "command": "exit",
            "user_id": user_id_2,
            "room_id": 1,
        }

        # EXPECTED: 정상적으로 방에 입장되었을 때 데이터 값, 정상적으로 방에서 퇴장되었을 때 데이터 값
        expected_enter = [user_id_1, user_id_2]
        expected_exit = [user_id_1]

        # WHEN: 방을 생성하고, 방에 입장하고, 방에서 퇴장하고, 메시지를 받는다.
        await self.communicator.send_json_to(create_command)
        # 방 생성 커맨드에 대한 응답은 받지 않는다.
        _ = await self.communicator.receive_json_from()

        await self.communicator.send_json_to(enter_command)
        enter_response = await self.communicator.receive_json_from()

        # user_1 이 받는 입장 정보는 무시한다.
        while enter_response['data']['type'] != 'room':
            enter_response = await self.communicator.receive_json_from()

        await self.communicator.send_json_to(exit_command)
        exit_response = await self.communicator.receive_json_from()

        # user_2가 받는 퇴장 정보는 무시한다.
        while exit_response['data']['type'] != 'room':
            exit_response = await self.communicator.receive_json_from()

        # user_1 이 받는 정상적인 퇴장 정보
        exit_response = await self.communicator.receive_json_from()
        while exit_response['data']['type'] != 'room':
            exit_response = await self.communicator.receive_json_from()

        # THEN: 방에 정상적으로 입장되었는지, 방에서 정상적으로 퇴장되었는지 확인한다.
        self.assertEqual(enter_response['data']['result']['participants'], expected_enter)
        self.assertEqual(exit_response['data']['result']['participants'], expected_exit)
