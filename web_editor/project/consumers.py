from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from asgiref.sync import async_to_sync
import json
from web_editor.wsgi import *
from .models import Project

class BasicConsumer(AsyncWebsocketConsumer):
    # for testing connection
    
    async def connect(self):
        await self.accept()
        
    async def disconnect(self, close_code):
        pass

class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self): 
        self.user = self.scope["user"]
        
        # TODO: check if user is allowed to access project

        self.project_id = self.scope['url_route']['kwargs']['pk']
        self.project_group_name = "project_" + self.project_id;
        
        # join room group
        await self.channel_layer.group_add(
            self.project_group_name, self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.project_group_name, self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        await self.channel_layer.group_send(
            self.project_group_name, {"type": "chat_message", "message": message}
        )
            
    async def chat_message(self, event):
        message = event["message"]
        
        await self.send(text_data = json.dumps({"message": message}))

class ProjectCreateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.project_id = Project.objects.filter(writer=self.user).last().id

        await self.channel_layer.group_add("project " + self.project_id, self.channel_name)
        await self.accept()