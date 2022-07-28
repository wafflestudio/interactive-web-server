from user.serializer import UserSerializer
from .models import Project
from rest_framework import serializers
from django.core.exceptions import ValidationError

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        return project
    
class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'html', 'css', 'js')
    
    def update(self, project, validated_data):
        super().update(project, validated_data)
        return project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
    writer = serializers.SerializerMethodField()
    
    def get_writer(self, obj):
        return UserSerializer(obj.writer).data