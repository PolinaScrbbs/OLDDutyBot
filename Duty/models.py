from django.db import models

class People(models.Model):
    full_name = models.CharField(max_length=100, unique=True, verbose_name='ФИО')

    #Количество дежурств человека
    @property
    def duty_count(self):
        return Duty.objects.filter(people=self).count()

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

