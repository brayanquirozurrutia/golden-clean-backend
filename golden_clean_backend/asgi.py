import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import service.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "golden_clean_backend.settings")

# Load Django ASGI application
django_asgi_app = get_asgi_application()

# Import the middleware after loading Django
from golden_clean_backend.middleware import QueryStringJWTAuthMiddleware

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": QueryStringJWTAuthMiddleware(
        URLRouter(
            service.routing.websocket_urlpatterns
        )
    ),
})
