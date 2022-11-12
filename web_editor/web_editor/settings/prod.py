from .base import *

DEBUG = False

ALLOWED_HOSTS = ['13.124.48.26', 'webgam-server.shop', 'wss://webgam-server.shop']

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_KEY")
AWS_S3_REGION_NAME = get_secret("AWS_S3_REGION_NAME")

AWS_STORAGE_BUCKET_NAME = get_secret("AWS_STORAGE_BUCKET_NAME")
#AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (
    #AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_S3_SIGNATURE_VERSION = 's3v4'