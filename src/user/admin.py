from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from django.utils.translation import gettext, gettext_lazy as _

# admin.site.register(User, UserAdmin)

@admin.register(User)
class AdminUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Channels'), {'fields': ('creator', 'can_edit_creator', 'can_edit_all_channel', 'creator_applied')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    filter_horizontal = ('groups', 'user_permissions')