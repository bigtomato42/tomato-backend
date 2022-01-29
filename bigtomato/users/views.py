# Django imports
from django.contrib.auth.models import User
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer

# DRF imports
# app imports


class UserViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    create:
    Create a user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Authenticate, unless you are creating a user"""
        return [AllowAny()] if self.action == "create" else [IsAuthenticated()]

    def list(self, request):
        """Returns an object of an authenticated user"""
        return Response(self.get_serializer(request.user).data)
