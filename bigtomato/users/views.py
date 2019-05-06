from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from conf.settings import local


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return UserSerializer(*args, **kwargs)

    def list(self, request):
        return Response(self.get_serializer(request.user).data)

    def create(self, request):
        username = request.data['username']
        password = request.data['password']
        name = request.data['name']
        new_user = User.objects.create_user(username=username, password=password, first_name=name)

        return Response(self.get_serializer(new_user).data)

    @action(detail=False, methods=['post'], url_path='log_in')
    def log_in(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.get(username=username)
        if user.check_password(password):
            return Response(self.get_serializer(user).data)

        else:
            return Response({"invalid username or pass"})
