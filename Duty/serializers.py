from rest_framework import serializers
from .models import People, Duty
from authorization.parser import get_group_list

class PeopleSerializer(serializers.ModelSerializer):
    duties_count = serializers.IntegerField(default=0)

    class Meta:
        model = People
        fields = ['id', 'full_name', 'group', 'duties_count']

    def validate_group(self, value):
        groups_list = get_group_list()
        if value not in groups_list:
            raise serializers.ValidationError(f'Недопустимое значение группы. Доступные группы: {", ".join(groups_list)}')
        return value
  
class DutySerializer(serializers.ModelSerializer):
    people = PeopleSerializer()
    class Meta:
        model = Duty
        fields = '__all__'


