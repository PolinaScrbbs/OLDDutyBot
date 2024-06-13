from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from rest_framework.authtoken.models import Token as AbstractToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .parser import get_group_list

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)
    
class Role(models.Model):
    title = models.CharField(_("Название"), max_length=50)

    class Meta:
        verbose_name = _("Роль")
        verbose_name_plural = _("Роли")
        db_table = _("auth_role")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Role_deatil", kwargs={"pk": self.pk})

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("Имя пользователя"), max_length=20, unique=True)
    password = models.CharField(_("Пароль"), max_length=128)
    role = models.ForeignKey(Role, models.CASCADE, verbose_name=_("Роль"), default=3)
    full_name = models.CharField(_('ФИО'), max_length=70)
    group = models.CharField(_('Группа'), max_length=10, null=True, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        db_table = _("auth_user")

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("User_deatil", kwargs={"pk": self.pk})

    def clean(self):
        super().clean()
        groups_list = get_group_list()
        if self.group.lower() not in groups_list:
            raise ValidationError({'group': f'Недопустимое значение группы. Доступные группы: {", ".join(groups_list)}'})
        else:
            self.group = self.group.upper()

class Token(AbstractToken):
    class Meta(AbstractToken.Meta):
        verbose_name = _("Токен")
        verbose_name_plural = _("Токены")
        db_table = _("auth_token")

class TokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            prefix, key = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None
        except ValueError:
            return None

        try:
            token = Token.objects.get(key=key)
            user = token.user
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return (user, None)      
