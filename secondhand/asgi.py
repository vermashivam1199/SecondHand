"""
ASGI config for secondhand project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_patterns as chat_ws_patterns
from notification.routing import websocket_patterns as notification_ws_patterns
from user_profile.routing import websocket_patterns as dashboard_ws_patterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secondhand.settings")


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter([
    *chat_ws_patterns,
    *notification_ws_patterns,
    *dashboard_ws_patterns
        ])
    )
})