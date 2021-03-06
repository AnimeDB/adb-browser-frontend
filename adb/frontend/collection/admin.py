from django.contrib import admin
from adb.frontend.collection.models import Genre, Actor, Movie, Link, Service, Release

class GenreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Genre, GenreAdmin)

class ActorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Actor, ActorAdmin)

class MovieAdmin(admin.ModelAdmin):
    pass
admin.site.register(Movie, MovieAdmin)

class ServiceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Service, ServiceAdmin)

class LinkAdmin(admin.TabularInline):
    model = Link

class ReleaseAdmin(admin.ModelAdmin):
    inlines = [
        LinkAdmin,
    ]
admin.site.register(Release, ReleaseAdmin)