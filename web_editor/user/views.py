from django.forms import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializer import *
from .models import User


class UserCreateViewSet(GenericViewSet):
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(data={'user': self.get_serializer(user).data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data=e, status=400)


class UserLoginViewSet(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response(status=status.HTTP_403_FORBIDDEN, data='아이디나 패스워드가 일치하지 않습니다.')
