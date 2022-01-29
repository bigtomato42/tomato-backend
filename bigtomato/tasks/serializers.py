from rest_framework import serializers

from .models import Task
from bigtomato.groups.models import Group


class TaskSerializer(serializers.ModelSerializer):

    description = serializers.CharField(required=False)
    finished = serializers.BooleanField(required=False)
    group = serializers.PrimaryKeyRelatedField(many=False, queryset=Group.objects.all())

    class Meta:
        model = Task
        fields = "__all__"
