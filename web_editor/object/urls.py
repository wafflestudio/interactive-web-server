from django.urls import include, path
from rest_framework import routers

from object.views import ObjectViewSet

router = routers.SimpleRouter()
router.register('objects', ObjectViewSet, basename='object')

urlpatterns = [
    path('', include(router.urls)),
]
