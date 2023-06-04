from django.urls import path

from lobby.consumers import LobbyConsumer

websocket_urlpatterns = [
    path("", LobbyConsumer.as_asgi()),
    # path("<int:pk>", RoomConsumer.as_asgi())
]
