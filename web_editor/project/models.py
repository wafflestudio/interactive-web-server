from django.db import models

from common.common import CustomModelManager, file_upload_path
from user.models import User

# Create your models here.
class Project(models.Model):
    objects = CustomModelManager()
    
    title = models.CharField(max_length=30)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    html = models.FileField(upload_to=file_upload_path, blank=True)
    js = models.FileField(upload_to=file_upload_path, blank=True)
    css = models.FileField(upload_to=file_upload_path, blank=True)