from rest_framework import serializers

from .models import Object


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'

    def create(self, validated_data):
        instance = Object.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance
