from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    token = serializers.SerializerMethodField()
    name = serializers.CharField(source='first_name')

    def get_token(self, obj):
        return obj.auth_token.key
