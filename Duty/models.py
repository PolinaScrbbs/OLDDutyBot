from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Duty(models.Model):
    attendant = models.ForeignKey(get_user_model(), models.CASCADE, verbose_name=_('Дежурный'))
    date = models.DateField(_('Дата дежурства'), default=timezone.now)

    class Meta:
        verbose_name = _('Дежурство')
        verbose_name_plural = _('Дежурства')
        db_table = "duties"

    def __str__(self):
        return f"{self.attendant.full_name} - {self.date}"
    
    def get_absolute_url(self):
        return reverse("Duty_detail", kwargs={"pk": self.pk})

