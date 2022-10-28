from django.db import models

from common.common import CustomModelManager
from common.models import TimeModel
from user.models import User


class Object(TimeModel):
    objects = CustomModelManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    tag = models.JSONField(default=dict)
    visibility = models.BooleanField(default=True)
    z_index = models.IntegerField()

    RECTANGLE = 'RE'
    ELLIPSE = 'EL'
    PATH = 'PA'
    DRAWING = 'DR'
    IMAGE = 'IM'
    TEXT = 'TE'
    SVG_TYPE_CHOICES = [
        (RECTANGLE, 'Rectangle'),
        (ELLIPSE, 'Ellipse'),
        (PATH, 'Path'),
        (DRAWING, 'Drawing'),
        (IMAGE, 'Image'),
        (TEXT, 'Text'),
    ]
    svg_type = models.CharField(max_length=2, choices=SVG_TYPE_CHOICES)
    fill = models.CharField(max_length=30)
    stroke = models.CharField(max_length=30)
    d_string = models.CharField(max_length=500)
    src_url = models.URLField()

    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()

