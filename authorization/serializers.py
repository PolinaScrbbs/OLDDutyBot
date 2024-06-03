from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from authorization.parser import get_group_list
from .models import Role, User, Token

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserDetailSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'group', 'full_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'group', 'full_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        group = validated_data.get('group', '').upper()
        if group not in get_group_list():
            raise ValidationError(f'Группа {group} не найдена')
        validated_data['group'] = group
        return super().create(validated_data)
