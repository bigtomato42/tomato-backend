from rest_framework import serializers
from .models import Group, Task


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    name = serializers.CharField(source='first_name')

    def get_token(self, obj):
        return obj.auth_token.key


class GroupSerializer(serializers.ModelSerializer):

    users = UserSerializer(read_only=True, many=True)

    class Meta:

        model = Group
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user

        obj = super(GroupSerializer, self).create(validated_data)
        obj.users.add(user)
        obj.save()
        return obj


class TaskSerializer(serializers.ModelSerializer):

    group = GroupSerializer(read_only=True, many=False)
    description = serializers.CharField(required=False)
    finished = serializers.BooleanField(required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):

        validated_data['group'] = self.context['group']
        obj = super(TaskSerializer, self).create(validated_data)

        return obj
