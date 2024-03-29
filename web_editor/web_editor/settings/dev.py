from .base import *

DEBUG = False

ALLOWED_HOSTS = ['webgam-api-dev.wafflestudio.com', 'wss://webgam-api-dev.wafflestudio.com']

DEFAULT_FILE_STORAGE = 'web_editor.storage_backends.MediaStorage'
STATICFILES_STORAGE = 'web_editor.storage_backends.BuildStorage'

AWS_S3_REGION_NAME = get_secret("AWS_S3_REGION_NAME")

AWS_STORAGE_BUCKET_NAME = get_secret("AWS_STORAGE_BUCKET_NAME")
#AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (
    #AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_S3_SIGNATURE_VERSION = 's3v4'
