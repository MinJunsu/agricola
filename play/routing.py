from django.urls import path

from play.consumers import GameConsumer

websocket_urlpatterns = [
    path("<int:pk>", GameConsumer.as_asgi())
]
