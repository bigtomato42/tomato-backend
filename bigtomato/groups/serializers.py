from django.urls import reverse
from rest_framework import serializers
from rest_framework.utils.urls import replace_query_param

from .models import Group


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    name = serializers.CharField(source="first_name")

    def get_token(self, obj):
        return obj.auth_token.key


class GroupSerializer(serializers.ModelSerializer):

    users = UserSerializer(read_only=True, many=True)
    owner = UserSerializer(read_only=True)
    pending_invitations = UserSerializer(read_only=True, many=True)
    tasks = serializers.SerializerMethodField()

    class Meta:

        model = Group
        fields = "__all__"

    def create(self, validated_data):
        owner = self.context["request"].user
        return Group.objects.create_group(owner, validated_data)

    def get_tasks(self, obj):
        request = self.context["request"]
        url = request.build_absolute_uri(reverse("tasks-list"))
        return replace_query_param(url=url, key="group", val=obj.pk)
