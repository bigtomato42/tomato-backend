# DRF imports
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer

# app imports


class CanViewAndEditTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.group.users.all()


class TaskViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return a given task

    list:
    List all the tasks for a user (for all groups). Use query param 'group' to filter by specific group

    create:
    Create a new task.

    update:
    Update task.

    delete:
    Delete task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, CanViewAndEditTask]

    def get_queryset(self):
        filter_params = {"group__users": self.request.user}
        if "group" in self.request.GET:
            filter_params.update({"group__pk": self.request.GET["group"]})
        return Task.objects.filter(**filter_params)
