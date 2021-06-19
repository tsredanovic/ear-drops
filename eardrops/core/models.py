from core.storage import CleanFileNameStorage
from django.db import models


def spaced_filename(instance, filename):
    return 'songs/{}'.format(filename)


class Song(models.Model):
    title = models.CharField(max_length=200, blank=False)

    artist = models.ForeignKey(
        'core.Artist',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='songs'
    )

    album = models.ForeignKey(
        'core.Album',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='songs'
    )

    file = models.FileField(
        null=False, blank=False,
        upload_to=spaced_filename,
        storage=CleanFileNameStorage
    )

    IMPORT = 'import'
    YOUTUBE = 'youtube'
    SOURCE_CHOICES = (
        (IMPORT, 'Import'),
        (YOUTUBE, 'Youtube'),
    )
    source = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=SOURCE_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.artist.name, self.title)


class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=200, blank=False)

    artist = models.ForeignKey(
        'core.Artist',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='albums'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
