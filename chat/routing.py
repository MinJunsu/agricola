from django.urls import path

from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path("<int:pk>/<int:user>", ChatConsumer.as_asgi()),
]
