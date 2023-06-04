from channels.routing import URLRouter
from django.urls import path

from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from lobby.routing import websocket_urlpatterns as lobby_websocket_urlpatterns
from play.routing import websocket_urlpatterns as play_websocket_urlpatterns

websocket_urlpatterns = URLRouter([
    path('ws/v1/', URLRouter([
        path('chat/', URLRouter(chat_websocket_urlpatterns)),
        path('play/', URLRouter(play_websocket_urlpatterns)),
        path('lobby', URLRouter(lobby_websocket_urlpatterns)),
    ])),
])
