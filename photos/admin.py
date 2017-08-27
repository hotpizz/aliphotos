from django.contrib import admin

from photos.models import Photo, Like, Flag

admin.site.register(Photo)
admin.site.register(Like)
admin.site.register(Flag)
