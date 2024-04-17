from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Admin

from django.contrib.auth.hashers import make_password

class AdminSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Admin
        fields = ['id', 'email', 'password', 'full_name']

        extra_kwargs = {
            'password': {'write_only': True},
        }

    #Хеширование пароля
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        admin = super(AdminSerializer, self).create(validated_data)
        Token.objects.create(user=admin)
        return admin