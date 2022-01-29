# django imports
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password as val_pass
from django.core import validators
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# DRF imports


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(source="first_name", required=False)

    class Meta:
        model = User
        fields = ("username", "email", "name", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_email(self, value):
        validators.validate_email(value)
        return value

    def validate_password(self, value):
        val_pass(value)  # use django validate password method using password validators in settings
        return value
