from django.db import models

from common.common import CustomModelManager, file_upload_path
from common.models import TimeModel
from user.models import User
from project.models import Project
from web_editor.storage_backends import MediaStorage


class Object(TimeModel):
    objects = CustomModelManager()

    object_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    
    tag = models.JSONField(default=dict)
    visibility = models.BooleanField(default=True)
    z_index = models.IntegerField()
    opacity = models.FloatField(default=1.0)

    src_url = models.URLField()

    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    
    image = models.FileField(storage=MediaStorage(), upload_to=file_upload_path, blank=True)

