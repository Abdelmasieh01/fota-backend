import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fota.settings')
from django.core.asgi import get_asgi_application
import django
django_asgi_app = get_asgi_application()
django.setup()

from customer_service.routing import websocket_urlpatterns
from customer_service.middleware import TokenAuthMiddleware


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns))
        )
    ),
})
