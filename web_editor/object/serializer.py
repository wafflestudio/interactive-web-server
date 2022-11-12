from rest_framework import serializers

from .models import Object
from project.serializer import ProjectSerializer


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'
        
    project = serializers.SerializerMethodField()
    
    def get_project(self, obj):
        return ProjectSerializer(obj.project).data

class ObjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'

    def create(self, validated_data):
        instance = Object.objects.create(**validated_data)
        return instance
    
class ObjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        exclude = ['user', 'project']
        
    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance
    