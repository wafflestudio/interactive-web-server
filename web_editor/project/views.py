from django.db import IntegrityError
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator

from .serializer import *
#from web_editor.wsgi import sio
# Create your views here.
class ProjectCreateView(APIView):
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['writer'] = request.user.id
        serializer = ProjectCreateSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            project = serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=ProjectSerializer(project).data)
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)
        
    def get(self, request, *args, **kwargs):
        page_number = request.query_params.get('page', 1)
        per_page = request.query_params.get('per_page', 8)
        projects = Project.objects.all()
        paginator = Paginator(projects, per_page)
        page = paginator.get_page(page_number)
        page_projects = page.object_list
        page_info = {
            "page": {
                "current": page.number,
                "has_next": page.has_next(),
                "has_previous": page.has_previous()
            },
            "data": ProjectSerializer(page_projects, many=True).data
        }
        return Response(status=status.HTTP_200_OK, data=page_info)
        
class ProjectUpdateView(APIView):

    def get(self, request, pk=None):
        project = Project.objects.filter(id=pk) if pk != 'me' else Project.objects.filter(writer=request.user)
        if not project and pk != 'me':
            return Response(status=status.HTTP_400_BAD_REQUEST, data="해당 id 값에 대응되는 프로젝트가 없습니다.")
        return Response(status=status.HTTP_200_OK, data=ProjectSerializer(project, many=True).data)

    def put(self, request, pk=None):
        project = Project.objects.get_or_none(id=pk)
        if not project:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="해당 id 값에 대응되는 프로젝트가 없습니다.")
        
        serializer = ProjectUpdateSerializer(project, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.update(project, serializer.validated_data)
            return Response(status=status.HTTP_200_OK, data=ProjectSerializer(project).data)
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)

    def delete(self, request, pk=None):
        project = Project.objects.get_or_none(id=pk)
        if not project:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="해당 id 값에 대응되는 프로젝트가 없습니다.")
        
        project.delete()
        return Response(status=status.HTTP_200_OK, data={"success" : True})
