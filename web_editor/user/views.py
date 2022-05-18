from django.contrib.auth import authenticate, login
from django.contrib.auth.models import update_last_login
from django.db import IntegrityError
from django.views import View
from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
import json

from .serializer import *


class UserSignUpView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=UserCreateSerializer(user).data)
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)
        except IntegrityError as e:
            return Response(status=status.HTTP_409_CONFLICT, data=e)


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user:
            login(request, user)
            update_last_login(None, user)
            return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)
        return Response(status=status.HTTP_403_FORBIDDEN, data="아이디나 패스워드가 일치하지 않습니다.")

class CSRFCheckView(View):
    
    def get(self, request):
        token = request.COOKIES.get('csrftoken')
        data = {
            'csrftoken': token
        }
        if token:
            return HttpResponse(json.dumps(data), content_type = 'application/json')
        else:
            return HttpResponse(status=403)


class UserViewSet(GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, pk=None):
        user = request.user if pk == 'me' else self.get_object()
        return Response(status=status.HTTP_200_OK, data=self.get_serializer(user).data)

    def update(self, request, pk=None):
        if pk != 'me':
            return Response(status=status.HTTP_403_FORBIDDEN, data="다른 유저 정보를 수정할 수 없습니다.")

        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.update(user, serializer.validated_data)
            return Response(status=status.HTTP_200_OK, data=self.get_serializer(user).data)
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)
        except IntegrityError as e:
            return Response(status=status.HTTP_409_CONFLICT, data=e)

    def destroy(self, request, pk=None):
        if pk != 'me':
            return Response(status=status.HTTP_403_FORBIDDEN, data="다른 유저로 탈퇴할 수 없습니다.")

        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.delete(user)
        return Response(status=status.HTTP_200_OK)
