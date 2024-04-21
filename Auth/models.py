from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from .parser import get_group_list

class AdminManager(BaseUserManager):
    def create_user(self, full_name, password=None, **extra_fields):
        if not full_name:
            raise ValueError('Full_name is required')
        user = self.model(full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(full_name, password, **extra_fields)

class Admin(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=70, unique=True, verbose_name='ФИО')
    group = models.CharField(max_length=10, default='ИС-33К', verbose_name='Группа')
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
        if self.group.lower() not in groups_list:
            raise ValidationError({'group': f'Недопустимое значение группы. Доступные группы: {", ".join(groups_list)}'})
        else:
            self.group = self.group.upper()
