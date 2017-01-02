from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from project.models import QwirkUser

class UserProfileInline(admin.TabularInline):
    model = QwirkUser

class MyUserAdmin(UserAdmin):
    inlines = [
        UserProfileInline,
    ]

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)