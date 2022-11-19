from django.db import models

from common.common import CustomModelManager, file_upload_path
from user.models import User
from web_editor.storage_backends import BuildFileStorage

# Create your models here.
class Project(models.Model):
    objects = CustomModelManager()
    
    title = models.CharField(max_length=30)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    html = models.FileField(storage=BuildFileStorage(), upload_to=file_upload_path, blank=True)
    js = models.FileField(storage=BuildFileStorage(), upload_to=file_upload_path, blank=True)
    css = models.FileField(storage=BuildFileStorage(), upload_to=file_upload_path, blank=True)