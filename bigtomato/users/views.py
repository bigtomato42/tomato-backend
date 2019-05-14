# Django imports
from django.contrib.auth.models import User
# DRF imports
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# app imports
from .serializers import UserSerializer


class UserViewSet(ListModelMixin,
                  CreateModelMixin,
                  GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @permission_classes((IsAuthenticated))
    def list(self, request):
        """Returns an object of an authenticated user"""
        return Response(self.get_serializer(request.user).data)

    def create(self, request):
        """Creates a user"""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
