from django.urls import path

from play.consumers import GameConsumer

websocket_urlpatterns = [
    path("ws/game/<int:pk>", GameConsumer.as_asgi())
]
