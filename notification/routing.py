from .consumer import OfferedPriceConsumer
from django.urls import path

websocket_patterns = [
    path("ws/notification/", OfferedPriceConsumer.as_asgi())
]