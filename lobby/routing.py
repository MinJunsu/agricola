from django.urls import path

from lobby.consumers import LobbyConsumer, RoomConsumer

websocket_urlpatterns = [
    path("<int:pk>", LobbyConsumer.as_asgi()),
    path("<int:pk>/<int:user_id>", RoomConsumer.as_asgi())
]
