from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.admin import TokenAdmin as AbstractTokenAdmin
from .models import Role, User, Token

admin.site.unregister(Group)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'role', 'group', 'full_name')

@admin.register(Token)
class TokenAdmin(AbstractTokenAdmin):
    pass



