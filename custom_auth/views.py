from django_ratelimit.core import is_ratelimited
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate


def validate_input(username, password):
    """
    Validate input format for username and password.
    :param username: The email address of the user
    :param password: The password of the user
    :return: True if input is valid, False otherwise
    """
    import re
    # Allow only valid email format for username
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", username):
        return False

    # Allow alphanumeric and special characters for password
    if not re.match(r"^[A-Za-z0-9@#$%^&+=]{8,}$", password):
        return False

    return True


class LoginAPIView(APIView):
    """
    APIView to authenticate users and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Authenticate user and return JWT tokens.
        """

        # Rate limiting logic
        if is_ratelimited(request=request, group='login', key='ip', rate='5/m', method=['POST'], increment=True):
            return Response({"detail": "Rate limit exceeded. Please try again later."},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        username = request.data.get("username")
        password = request.data.get("password")

        # Validate input format (email and password)
        if not validate_input(username, password):
            return Response({"detail": "Invalid input format"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user:
            # Create JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": user.role,
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)