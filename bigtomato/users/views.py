# Django imports
from django.contrib.auth.models import User
# DRF imports
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny


# app imports
from .serializers import UserSerializer


class UserViewSet(ListModelMixin,
                  CreateModelMixin,
                  GenericViewSet):
    """
    create:
    Create a user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Authenticate, unless you are creating a user"""
        return [AllowAny()] if self.action == 'create' else [IsAuthenticated()]

    def list(self, request):
        """Returns an object of an authenticated user"""
        return Response(self.get_serializer(request.user).data)
