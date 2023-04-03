from .consumer import ChatConsumer
from django.urls import path

websocket_patterns = [
    path("ws/chat/<str:g_name>/", ChatConsumer.as_asgi())
]