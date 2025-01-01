from django.urls import re_path
from service.consumers import EmployeeConsumer

websocket_urlpatterns = [
    re_path(r'ws/employees/$', EmployeeConsumer.as_asgi()),
]
