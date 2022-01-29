from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes as permission_classes_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Group
from .serializers import GroupSerializer
from conf.settings import local


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsGroupUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.users.all()


class IsInvitedToGroup(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user, obj.pending_invitations.all())
        return request.user in obj.pending_invitations.all()


class GroupViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return a given group

    list:
    List all the groups for a given user.

    create:
    Create a new group, setting the authenticated user as a owner of the group.

    update:
    Update name or description of the group. Can only be done by the author

    delete:
    Delete the group.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Group.objects.filter(users=self.request.user)

    @permission_classes_decorator((IsAuthenticated, IsGroupUser))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=((IsAuthenticated, IsOwnerOrReadOnly)))
    def invite_users(self, request, *args, **kwargs):
        """Intite users to a group. Can only be done by the owner
        request body parameters : users: string
        users seperated by comma"""
        obj = self.get_object()
        self.check_object_permissions(self.request, obj)
        usernames = self.request.data["users"].split(",")
        users = User.objects.filter(username__in=usernames)
        obj.pending_invitations.add(*users)
        obj.save()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=((IsAuthenticated, IsOwnerOrReadOnly)))
    def pending_invitations(self, request, *args, **kwargs):
        """View pending invitations for groups"""
        user = self.request.user
        groups_with_invitations = Group.objects.filter(pending_invitations=user)
        serializer = self.get_serializer(groups_with_invitations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=((IsAuthenticated, IsInvitedToGroup)))
    def accept_invitation(self, request, pk):
        """Accept invitation to a group by user"""
        user = self.request.user
        obj = Group.objects.get(pk=pk)
        self.check_object_permissions(self.request, obj)
        obj.accept_invitation(user)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=((IsAuthenticated, IsGroupUser)))
    def leave(self, request, pk):
        user = self.request.user
        obj = Group.objects.get(pk=pk)
        self.check_object_permissions(self.request, obj)
        obj.users.remove(user)
        return Response({"left group": True})

    # @permission_classes_decorator((IsAuthenticated, IsOwner))
    # def update(self, request, *args, **kwargs):
    #     """Update name or description of the group"""
    #     #obj = self.get_object()
    #     #self.check_object_permissions(request, obj)
    #     return super(GroupViewSet, self).update(request, *args, **kwargs)

    # def get_tasks(self, request, pk):
    #     group = Group.objects.get(pk=pk)
    #     tasks = group.tasks.all()
    #     serializer = TaskSerializer(tasks, many=True)
    #     return Response(serializer.data)
    #
    # def create_task(self, request, pk):
    #     serializer = TaskSerializer(data=request.data, context={'group': Group.objects.get(pk=pk)})
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def update_task(self, request, pk):
    #     return None
    #
    # def delete_task(self, request, pk):
    #     return None
    #
    # @action(detail=True, methods=['get', 'post', 'put', 'delete'])
    # def tasks(self, request, pk):
    #     actions = {
    #                 'GET': self.get_tasks,
    #                 'POST': self.create_task,
    #                 'PUT': self.update_task,
    #                 'DELETE': self.delete_task
    #               }
    #
    #     if request.method in actions:
    #         return actions[request.method](request, pk)
