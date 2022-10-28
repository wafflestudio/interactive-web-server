from django.urls import path, include
from rest_framework import routers
from .views import *


urlpatterns = [
    path('project/', ProjectCreateView.as_view(), name='project'),
    path('project/<str:pk>/', ProjectUpdateView.as_view(), name='update_project'),
]
