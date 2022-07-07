from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('/ws/project/<str:pk>/', consumers.ProjectConsumer.as_asgi()),
]