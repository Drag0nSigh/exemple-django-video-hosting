from django.contrib.auth import get_user_model
from django.db import models

from core.constants import MAX_LENGTH_VIDEO_NAME, VIDEO_QUALITY_OPTIONS

User = get_user_model()


class Video(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор видео',
        related_name='videos',
        blank=False,
        null=False,
    )
    is_published = models.BooleanField(
        verbose_name='Признак опубликованности видео',
        blank=False,
        null=False,
    )
    name = models.CharField(
        verbose_name='Название видео',
        max_length=MAX_LENGTH_VIDEO_NAME,
        blank=False,
        null=False,
    )
    total_likes = models.IntegerField(
        verbose_name='Всего лайков',
        default=0,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата и время загрузки',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return self.name


class VideoFile(models.Model):
    video = models.ForeignKey(
        Video,
        verbose_name='Видео',
        related_name='video_files',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    file = models.FileField(
        upload_to='data/video/',
        blank=False,
        null=False,
    )
    quality = models.CharField(
        verbose_name='Качество',
        blank=False,
        null=False,
        choices=[(x, x) for x in VIDEO_QUALITY_OPTIONS],
        max_length=20,
    )

    class Meta:
        ordering = ('video',)
        verbose_name = 'Видео файл'
        verbose_name_plural = 'Видео файлы'

    def __str__(self):
        return self.video


class Like(models.Model):
    video = models.ForeignKey(
        Video,
        verbose_name='Видео которому поставили лайк',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='likes',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь поставивший лайк'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'video'], name='unique_user_video_like')
        ]
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'Пользователь {self.user.username} поставил лайк {self.video.name}'
