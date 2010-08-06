from django.contrib import admin
from django.contrib.auth import models


#class LinkAdmin(admin.TabularInline):
#    model = Link
admin.site.register(models.Permission)