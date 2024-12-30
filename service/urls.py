from django.urls import path
from service.views import ServiceRequestAPIView

urlpatterns = [
    path('request/', ServiceRequestAPIView.as_view(), name='service-request'),
]
