from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from conf.settings import local
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Group, Task
from .serializers import GroupSerializer, TaskSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_tasks(self, request, pk):
        group = Group.objects.get(pk=pk)
        tasks = group.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def create_task(self, request, pk):
        serializer = TaskSerializer(data=request.data, context={'group': Group.objects.get(pk=pk)})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update_task(self, request, pk):
        return None

    def delete_task(self, request, pk):
        return None

    @action(detail=True, methods=['get', 'post', 'put', 'delete'])
    def tasks(self, request, pk):
        actions = {
                    'GET': self.get_tasks,
                    'POST': self.create_task,
                    'PUT': self.update_task,
                    'DELETE': self.delete_task
                  }

        if request.method in actions:
            return actions[request.method](request, pk)
