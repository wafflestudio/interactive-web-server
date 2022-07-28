from django.db import models
import datetime
import os
import uuid

class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

def file_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    d = datetime.datetime.now()
    filepath = d.strftime("%Y/%m/%d")
    suffix = d.strftime("%Y%m%d%H%M%S")
    filename = "%s_%s_%s" % (uuid.uuid4().hex, suffix, ext)
    return os.path.join(filepath, filename)