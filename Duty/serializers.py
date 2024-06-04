from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import timezone


from .models import Duty
from authorization.serializers import UserDetailSerializer
from authorization.parser import get_group_list

class AttendantSerializer(serializers.ModelSerializer):
    duties_count = serializers.IntegerField(default=0)
    last_duty_date = serializers.SerializerMethodField()
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'full_name', 'group', 'duties_count', 'last_duty_date']

    def get_duties_count(self, obj):
        return Duty.objects.filter(duty=obj).count()
    
    def get_last_duty_date(self, obj):
        today = timezone.now().date()
        last_duty = Duty.objects.filter(duty=obj, date__lte=today).order_by('-date').first()
        return last_duty.date if last_duty else None

    def validate_group(self, value):
        groups_list = get_group_list()
        if value not in groups_list:
            raise serializers.ValidationError(f'Недопустимое значение группы. Доступные группы: {", ".join(groups_list)}')
        return value

# class DutyCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Duty
#         fields = ('duty')

class DutyDetailSerializer(serializers.ModelSerializer):
    duty = UserDetailSerializer()
    class Meta:
        model = Duty
        fields = '__all__'


