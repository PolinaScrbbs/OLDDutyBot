from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# class People(models.Model):
#     full_name = models.CharField(max_length=100, unique=True, verbose_name='ФИО')
#     group = models.CharField(max_length=10, blank=True, verbose_name='Группа')

#     @property
#     def duties_count(self):
#         duties_count = Duty.objects.filter(people=self).count()
#         return duties_count if duties_count else 0
    
#     @property
#     def last_duty_date(self):
#         today = timezone.now().date()
#         last_duty = Duty.objects.filter(people=self, date__lte=today).order_by('-date').first()
#         return last_duty.date if last_duty else None
    
#     def clean(self):
#         super().clean()
#         groups_list = get_group_list()
#         if self.group.lower() not in groups_list:
#             raise ValidationError({'group': f'Недопустимое значение группы. Доступные группы: {", ".join(groups_list)}'})
#         else:
#             self.group = self.group.upper()

#     class Meta:
#         verbose_name = 'Человек'
#         verbose_name_plural = 'Люди'

#     def __str__(self):
#         return self.full_name

class Duty(models.Model):
    duty = models.ForeignKey(get_user_model(), models.CASCADE, verbose_name=_('Дежурный'))
    date = models.DateField(_('Дата дежурства'), default=timezone.now)

    class Meta:
        verbose_name = _('Дежурство')
        verbose_name_plural = _('Дежурства')
        db_table = "duties"

    def __str__(self):
        return f"{self.duty.full_name} - {self.date}"
    
    def get_absolute_url(self):
        return reverse("Role_detail", kwargs={"pk": self.pk})

