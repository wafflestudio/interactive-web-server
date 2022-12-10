"""
ASGI config for web_editor project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_editor.settings.dev')
django.setup()

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from .middleware import JwtAuthMiddlewareStack
import project.routing
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        JwtAuthMiddlewareStack(
            URLRouter([
                *project.routing.websocket_urlpatterns,
            ])
        )
        #["wss://webgam-server.shop", "ws://127.0.0.1:8000", "ws://localhost:8000"]        
    )
})
