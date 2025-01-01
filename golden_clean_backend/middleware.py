from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.db import close_old_connections
from django.contrib.auth import get_user_model

User = get_user_model()

class QueryStringJWTAuthMiddleware:
    """
    Middleware that authenticates users based on a JWT token passed in the query string.
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        """
        Call the middleware with the given scope, receive and send
        :param scope: The scope of the middleware
        :param receive: The reception of the middleware
        :param send: To send of the middleware
        :return:
        """
        close_old_connections()
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        if token:
            try:
                validated_token = AccessToken(token)
                user = await self.get_user(validated_token["user_id"])
                scope["user"] = user if user else AnonymousUser()
            except Exception as e:
                print(f"JWT Error: {e}")
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)

    @staticmethod
    async def get_user(user_id):
        """
        Get the user from the database
        :param user_id: The user ID
        :return: The user
        """
        try:
            return await database_sync_to_async(User.objects.get)(id=user_id)
        except User.DoesNotExist:
            return None
