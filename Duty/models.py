from django.db import models
from Auth.parser import get_group_list
from django.core.exceptions import ValidationError

class People(models.Model):
    full_name = models.CharField(max_length=100, unique=True, verbose_name='ФИО')
    group = models.CharField(max_length=10, verbose_name='Группа')

    #Количество дежурств человека
    @property
    def duty_count(self):
        return Duty.objects.filter(people=self).count()
    
    def clean(self):
        super().clean()
        groups_list = get_group_list()
        if self.group not in groups_list:
            raise ValidationError({'group': f'Недопустимое значение группы. Доступные группы: {", ".join(groups_list)}'})

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'

    def __str__(self):
        return self.full_name

class Duty(models.Model):
    people = models.ForeignKey(People, related_name='duties', on_delete=models.CASCADE, verbose_name='Человек')
    date = models.DateField(verbose_name='Дата дежурства')

    class Meta:
        verbose_name = 'Дежурство'
        verbose_name_plural = 'Дежурства'

    def __str__(self):
        return f"{self.people.full_name} - {self.date}"

