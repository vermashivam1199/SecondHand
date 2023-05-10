from .consumer import DashboardConsumer
from django.urls import path

websocket_patterns = [
    path("ws/dashboard/", DashboardConsumer.as_asgi())
]