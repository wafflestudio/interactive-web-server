from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', UserSignUpView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    #path('verify/', CSRFCheckView.as_view())
]
