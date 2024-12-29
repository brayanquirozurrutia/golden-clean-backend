from django.urls import path
from custom_auth.views import LoginAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
]

