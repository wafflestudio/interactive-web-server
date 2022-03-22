from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', UserCreateViewSet.as_view()),
    path('login/', UserLoginViewSet.as_view()),
]