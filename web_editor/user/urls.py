from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('signup', UserCreateViewSet, basename='signup')

urlpatterns = [
    path('', include(router.urls), name='signup'),
    path('login/', UserLoginViewSet.as_view()),
]