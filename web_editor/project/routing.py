from django.urls import path, re_path
from channels.routing import URLRouter
from . import consumers
from web_editor.wsgi import *

websocket_urlpatterns = [
    #re_path(r"ws/project/$", consumers.ProjectCreateConsumer.as_asgi()),
    re_path(r"ws/project/(?P<pk>\d+)/$", consumers.ProjectConsumer.as_asgi()),
    re_path(r"ws/ping/", consumers.BasicConsumer.as_asgi())
]
