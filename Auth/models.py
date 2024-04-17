from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from .parser import get_group_list

class AdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Admin(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=70, unique=True, verbose_name='ФИО')
    group = models.CharField(max_length=10, verbose_name='Группа')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AdminManager()

    USERNAME_FIELD = 'full_name'

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'

    def __str__(self):
        return self.full_name

    def clean(self):
        super().clean()
        groups_list = get_group_list()
        if self.group not in groups_list:
            raise ValidationError({'group': f'Недопустимое значение группы. Доступные группы: {", ".join(groups_list)}'})
