from channels.generic.websocket import JsonWebsocketConsumer
from channels.auth import login
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
import json
from web_editor.wsgi import *
from .models import Project
from object.models import Object
from object.serializer import ObjectSerializer, ObjectCreateSerializer, ObjectUpdateSerializer
from common.websocket_template import WebsocketTemplate
from channels.db import database_sync_to_async
from rest_framework.exceptions import ValidationError, MethodNotAllowed, NotFound

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
        objects = self.get_project_objects() #async version: await sync_to_async(list)(query)
        data = ObjectSerializer(objects, many=True).data
        message = WebsocketTemplate.construct_message(method="GET", endpoint="/objects/", data=data)
        self.send_json(message)
        
    def receive_json(self, request):
        try:
            valid_request = WebsocketTemplate.validate_message(request)
        except (MethodNotAllowed, NotFound) as e:
            self.send_json({"error": e.detail})
            return
            
        method = valid_request.get("method")
        endpoint = valid_request.get("endpoint")
        url_params = valid_request.get("url_params")
        query_params = valid_request.get("query_params")
        data = valid_request.get("data")
        
        if method == "POST" and endpoint == "/objects/":
            self.create_object(data)
        elif method == "PATCH" and endpoint == "/objects/":
            if "id" not in url_params:
                self.send_json("No object id was given in url_params.")
            else: 
                self.edit_object(url_params["id"], data)
        elif method == "DELETE" and endpoint == "/objects/":
            if "id" not in url_params:
                self.send_json("No object id was given in url_params.")
            self.delete_object(url_params["id"], data)
    
    def create_object(self, data):
        data['user'] = self.user.id
        data['project'] = self.project_id
        serializer = ObjectCreateSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            message = WebsocketTemplate.construct_message(method="POST", endpoint="/objects/", data=ObjectSerializer(instance).data)
            self.broadcast("room.message", message)
        except ValidationError as e:
            self.send_json({"error": e.detail})
        
        
    def edit_object(self, id, data):
        instance = Object.objects.get_or_none(id=id, user=self.user)
        if instance is None:
            self.send_json({"error":"No object corresponding to id."})
            return
        if data.get('user', None) is not None:
            self.send_json({"error":"Changing object owner is not allowed."})
            return
        if data.get('project_name', None) is not None:
            self.send_json({"error": "Changing object's project is not allowed."})
            return
        serializer = ObjectUpdateSerializer(instance, data=data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.update(instance, serializer.validated_data)
            message = WebsocketTemplate.construct_message(
                method="PATCH", endpoint="/objects/", url_params={"id": id}, data=ObjectSerializer(instance).data
                )
            self.broadcast("room.message", message)
        except ValidationError as e:
            self.send_json({"error": e.detail})
        
        
    def delete_object(self, id, data):
        instance = Object.objects.get_or_none(id=id, user=self.user)
        if instance is None:
            return self.send_json({"error": "No object corresponding to id."})

        instance.delete()
        data = {"success": True, "object": ObjectSerializer(instance).data}
        
        message = WebsocketTemplate.construct_message(
                method="DELETE", endpoint="/objects/", url_params={"id": id}, data=data
                )
        self.broadcast("room.message", message)
    
    
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