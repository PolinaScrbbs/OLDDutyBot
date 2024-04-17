from rest_framework import serializers
from .models import People, Duty

class DutySerializer(serializers.ModelSerializer):
    class Meta:
        model = Duty
        fields = '__all__'

class PeopleSerializer(serializers.ModelSerializer):
    duty_count = serializers.IntegerField()

    class Meta:
        model = People
        fields = ['id', 'full_name', 'duty_count']


