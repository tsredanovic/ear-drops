from django.db import models

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
        null=False, blank=False
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


class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False)


class Album(models.Model):
    name = models.CharField(max_length=200, blank=False)

    artist = models.ForeignKey(
        'core.Artist',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='albums'
    )
