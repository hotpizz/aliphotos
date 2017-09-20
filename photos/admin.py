from django.contrib import admin

from photos.models import Photo, Like, Flag


@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo_preview']
    ordering = ['-created']
    actions = ['remove_complained_photos']

    def photo_preview(self, obj):
        if obj.photo:
            return '<img src="{}" width=200>'.format(obj.photo.url)
        return 'No photo, probably it was deleted before by another report.'
    photo_preview.allow_tags = True

    def remove_complained_photos(self, request, queryset):
        """Remove photo by report and then remove that flag."""
        for flag in queryset:
            if flag.photo:
                flag.photo.delete()
                flag.delete()
        self.message_user(request, 'All flags and its complained photos were deleted.')

admin.site.register(Photo)
admin.site.register(Like)
