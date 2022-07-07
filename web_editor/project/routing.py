from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('project/<str:pk>/', consumers.ProjectConsumer.as_asgi()),
]