from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from authorization.parser import get_group_list


class People(models.Model):
    full_name = models.CharField(max_length=100, unique=True, verbose_name='ФИО')
    group = models.CharField(max_length=10, blank=True, verbose_name='Группа')

    @property
    def duties_count(self):
        duties_count = Duty.objects.filter(people=self).count()
        return duties_count if duties_count else 0
    
    @property
    def last_duty_date(self):
        today = timezone.now().date()
        last_duty = Duty.objects.filter(people=self, date__lte=today).order_by('-date').first()
        return last_duty.date if last_duty else None
    
    def clean(self):
        super().clean()
        groups_list = get_group_list()
        if self.group.lower() not in groups_list:
            raise ValidationError({'group': f'Недопустимое значение группы. Доступные группы: {", ".join(groups_list)}'})
        else:
            self.group = self.group.upper()

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

