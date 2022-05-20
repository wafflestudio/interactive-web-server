from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', UserSignUpView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('verify/', CSRFCheckView.as_view())
]
