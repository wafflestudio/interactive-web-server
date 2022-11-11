from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from object.models import Object
from object.serializer import ObjectSerializer, ObjectCreateSerializer, ObjectUpdateSerializer
from project.models import Project


class ObjectViewSet(GenericViewSet):
    #serializer_class = ObjectSerializer
    queryset = Object.objects.all()

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.pk
        data['project'] = Project.objects.get(title=data["project_name"]).pk
        serializer = ObjectCreateSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=ObjectSerializer(instance).data)
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e.detail)

    def list(self, request):
        project_name = request.query_params.get('project_name')
        instances = self.get_queryset().filter(project_name=project_name, user=request.user)
        if len(instances) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND, data="해당 프로젝트에 오브젝트가 없습니다.")
        return Response(status=status.HTTP_200_OK, data=ObjectSerializer(instances, many=True).data)

    def retrieve(self, request, pk=None):
        instance = Object.objects.get_or_none(id=pk, user=request.user)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data="해당 id 값에 대응되는 오브젝트가 없습니다.")
        return Response(status=status.HTTP_200_OK, data=ObjectSerializer(instance).data)

    def partial_update(self, request, pk=None):
        instance = Object.objects.get_or_none(id=pk, user=request.user)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data="해당 id 값에 대응되는 오브젝트가 없습니다.")
        if request.data.get('user', None) is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="오브젝트의 소유자를 바꿀 수 없습니다.")
        if request.data.get('project_name', None) is not None or request.data.get('project', None) is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="오브젝트가 속한 프로젝트를 바꿀 수 없습니다.")

        serializer = ObjectUpdateSerializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.update(instance, serializer.validated_data)
            return Response(status=status.HTTP_200_OK, data=ObjectSerializer(instance).data)
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e.detail)

    def destroy(self, request, pk=None):
        instance = Object.objects.get_or_none(id=pk, user=request.user)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data="해당 id 값에 대응되는 오브젝트가 없습니다.")

        instance.delete()
        return Response(status=status.HTTP_200_OK, data={"success": True, "object": ObjectSerializer(instance).data})
