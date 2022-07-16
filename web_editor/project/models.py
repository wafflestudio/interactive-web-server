from django.db import models

from common.common import CustomModelManager
from user.models import User

# Create your models here.
class Project(models.Model):
    objects = CustomModelManager()
    
    title = models.CharField(max_length=30)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)