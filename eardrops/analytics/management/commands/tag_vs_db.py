import logging

from django.core.management.base import BaseCommand
import eyed3

from core.models import *


class Command(BaseCommand):
    """
    Compare song's data on file to database

    Description:
        Compares tag values of (`artist`, `album`, `title`) on a song file against the same values stored in database for every song. Prints out any inconsistencies.

    Example call:
        python manage.py tag_vs_db
    """

    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        # Get songs
        songs = Song.objects.select_related('artist').select_related('album').all()

        # Compare tags to DB
        for song in songs:
            tag = eyed3.load(song.file.path).tag

            db_artist = song.artist.name if song.artist else None
            db_album = song.album.name if song.album else None
            db_title = song.title
            if db_artist == tag.artist and db_album == tag.album and db_title == tag.title:
                continue

            self.logger.info('Missmatch on song: {} - {}\n\tArtist | DB: {} | Tag: {}\n\tTitle | DB: {} | Tag: {}\n\tAlbum | DB: {} | Tag: {}'.format(
                song.id, song.file, song.artist.name, tag.artist, song.title, tag.title, song.album.name, tag.album
            ))
