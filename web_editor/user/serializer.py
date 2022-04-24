from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'username',
            'password',
            'email',
            'date_joined',
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'username',
            'email',
            'date_joined',
        )

    @transaction.atomic
    def update(self, user, validated_data):
        if validated_data.get('user_id') is not None:
            raise ValidationError("ID는 변경할 수 없습니다.")
        if validated_data.get('date_joined') is not None:
            raise ValidationError("가입날짜는 변경할 수 없습니다.")

        super().update(user, validated_data)
        return user

    def delete(self, user):
        super().update(user, {'is_active': False})
        return user


