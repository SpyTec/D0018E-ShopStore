from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _

from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'personal_id',
                'phone_number',
            )
        }),
        (_('Address'), {
            'fields': (
                'address',
                'city',
                'zip_code',
            )
        }),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'personal_id',
                'phone_number',
            )
        }),
        (_('Address'), {
            'fields': (
                'address',
                'city',
                'zip_code',
            )
        }),
    )


admin.site.register(User, MyUserAdmin)
