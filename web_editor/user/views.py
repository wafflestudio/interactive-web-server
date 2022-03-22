from django.forms import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView

from .serializer import UserCreateSerializer
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class UserCreateViewSet(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(data = {'user' : UserCreateSerializer(user).data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data=e, status=400)

class UserLoginViewSet(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user == None:
            return Response(data = {'error' : '아이디나 비밀번호가 잘못되었습니다.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data = {'login' : True}, status=status.HTTP_200_OK)