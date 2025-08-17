from django.contrib import admin

from .models import Video, VideoFile, Like


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'is_published',
        'name',
        'total_likes',
        'created_at',
    )
    search_fields = ['name', 'is_published', 'owner__username']


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = (
        'video',
        'file',
        'quality',
    )
    search_fields = ['quality', 'video__name']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'video',
        'user',
    )
    search_fields = ['user__username', 'video__name']
