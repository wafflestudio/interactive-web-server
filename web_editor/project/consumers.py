from channels.generic.websocket import JsonWebsocketConsumer
from channels.auth import login
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
import json
from web_editor.wsgi import *
from .models import Project
from object.models import Object
from object.serializer import ObjectSerializer
from common.websocket_template import WebsocketTemplate
from channels.db import database_sync_to_async
from rest_framework.exceptions import ValidationError

class BasicConsumer(JsonWebsocketConsumer):
    # for testing connection
    
    def connect(self):
        self.accept()
        
    def disconnect(self, close_code):
        pass

class ProjectConsumer(JsonWebsocketConsumer):
    
    # attributes:
    # (User) user, (int) project_id, (Project) project, (str) project_group_name, channel_layer
    
    def connect(self): 
        self.user = self.scope["user"]

        self.project_id = int(self.scope['url_route']['kwargs']['pk'])
        # search for project corresponding to id
        self.project = self.get_project()
        if not self.project:
            self.close()
        # TODO: check if user is allowed to access project
        self.project_group_name = "project_" + str(self.project_id);
        
        self.accept()
        
        # join room
        async_to_sync(self.channel_layer.group_add)(
            self.project_group_name, self.channel_name
        )
        
        # send object list
        self.send_objects()

    def disconnect(self, close_code):
        # leave room
        async_to_sync(self.channel_layer.group_discard)(
            self.project_group_name, self.channel_name
        )
        
    def send_objects(self):
        objects = self.get_project_objects() #await sync_to_async(list)(query)
        data = ObjectSerializer(objects, many=True).data
        # where to put query params?
        message = WebsocketTemplate.construct_message("POST", "/objects/", data)
        self.send_json(message)
        
    def receive_json(self, request):
        # TODO refactor (make parse function in websocket_template)
        print("receive json function")
        method = request.get("method", None)
        endpoint = request.get("endpoint", None)
        data = request.get("data", None)
        
        if method == "POST" and endpoint == "/objects/":
            self.create_object(data)
    
    def create_object(self, data):
        print("create object function")
        data['user'] = self.user.id
        data['project'] = self.project_id
        serializer = ObjectSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            message = WebsocketTemplate.construct_message("POST", "/objects/", serializer.data)
            self.broadcast("room.message", message)
        except ValidationError as e:
            self.send_json({"error": e.detail})
    
    def broadcast(self, type, message):
        print("broadcast function")
        async_to_sync(self.channel_layer.group_send)(
            self.project_group_name, {"type": type, "message": message}
        )
    
    def room_message(self, event):
        print("room_message function")
        self.send_json(event["message"])
        
        
    def get_project(self):
        return Project.objects.get_or_none(id=self.project_id)
    
    def get_project_objects(self):
        return Object.objects.filter(project=self.project)
            

class ProjectCreateConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.project_id = Project.objects.filter(writer=self.user).last().id

        self.channel_layer.group_add("project " + self.project_id, self.channel_name)
        self.accept()