from django.contrib import admin
from adb.frontend.collection.models import List

class ListAdmin(admin.ModelAdmin):
    pass
admin.site.register(List, ListAdmin)