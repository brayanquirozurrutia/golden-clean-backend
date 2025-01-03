from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from custom_auth.views import LoginAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

