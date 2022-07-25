from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from web_editor.wsgi import *
from .models import Project

class ProjectConsumer(WebsocketConsumer):
    def connect(self): # send id
        self.user = self.scope["user"]
        # check if user is allowed to access project - How?
        self.project_id = self.scope['url_route']['kwargs']['pk']

        async_to_sync(self.channel_layer.group_add)("project " + self.project_id, self.channel_name)
        self.accept()

    def disconnect(self, id, close_code): # send id
        async_to_sync(self.channel_layer.group_discard)("project" + self.project_id, self.channel_name)

class ProjectCreateConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.project_id = Project.objects.filter(writer=self.user).last().id

        async_to_sync(self.channel_layer.group_add)("project " + self.project_id, self.channel_name)
        self.accept()