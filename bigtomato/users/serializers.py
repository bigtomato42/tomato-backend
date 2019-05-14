from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.core import validators


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(source='first_name', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_email(self, value):
        validators.validate_email(value)
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('Password needs to be atleast 6 characters')
        return value
