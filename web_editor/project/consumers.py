from channels.generic.websocket import WebsocketConsumer
from channels.auth import login
from asgiref.sync import async_to_sync
from web_editor.wsgi import *
from .models import Project

class BasicConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()
        
    def disconnect(self, close_code):
        pass

class ProjectConsumer(WebsocketConsumer):
    def connect(self): 
        self.user = self.scope["user"]
        
        # check if user is allowed to access project - How?
        self.accept()

        self.project_id = self.scope['url_route']['kwargs']['pk']
        print("project_id: ", self.project_id)

        async_to_sync(self.channel_layer.group_add)("project_" + self.project_id, self.channel_name)

        self.scope["session"].save()

    def disconnect(self, id, close_code):
        async_to_sync(self.channel_layer.group_discard)("project" + self.project_id, self.channel_name)

class ProjectCreateConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.project_id = Project.objects.filter(writer=self.user).last().id

        async_to_sync(self.channel_layer.group_add)("project " + self.project_id, self.channel_name)
        self.accept()