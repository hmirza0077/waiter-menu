"""
ASGI config for waiters project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from menu.consumers import WaitingConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waiters.settings')


# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('waiting', WaitingConsumer.as_asgi())
        ])
    )
})
