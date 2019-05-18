from rest_framework import serializers
from bigtomato.groups.models import Group
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    description = serializers.CharField(required=False)
    finished = serializers.BooleanField(required=False)
    group = serializers.PrimaryKeyRelatedField(many=False, queryset=Group.objects.all())

    class Meta:
        model = Task
        fields = '__all__'
