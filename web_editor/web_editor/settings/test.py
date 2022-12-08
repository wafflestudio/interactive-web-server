from .base import *

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'ws://localhost:8000', 'ws://127.0.0.1:8000']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_ROOT = '/home/gahyun/interactive-web-server/media'
