from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from project.models import *


class UserProfileInline(admin.TabularInline):
    model = QwirkUser


class MyUserAdmin(UserAdmin):
    inlines = [
        UserProfileInline,
    ]


class QwirkUserAdmin(admin.ModelAdmin):
    list_display = ('bio', 'birthDate', 'contacts')
    """list_filter = (
    'robot__name', 'robot__shop__name', 'robot__shop__society__name', 'state', 'component', 'component_id',
    'time_transfer', 'time_log')"""

    def contacts(self, obj):
        return obj.contacts


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(QwirkUser)
admin.site.register(QwirkGroup)
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(Notification)
