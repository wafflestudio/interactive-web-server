from rest_framework import serializers
from .models import User

class UserCreateSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ("user_id", "username", "password")
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user