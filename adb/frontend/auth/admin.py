from django.contrib import admin
from django.contrib.auth import models
from adb.frontend.auth.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(models.Permission)