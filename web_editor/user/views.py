from django.forms import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .serializer import UserCreateSerializer
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class UserCreateViewSet(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(data = {'user' : UserCreateSerializer(user).data}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data=e, status=400)

    
    def get(self, request, *args, **kwargs):
        return Response({"users" : UserCreateSerializer(User.objects.all(), many=True).data}, status = status.HTTP_200_OK)
