import logging
import os

from django.core.management.base import BaseCommand
from django.core.files import File
from django.db import transaction
import eyed3

from core.helpers import manually_set_value
from core.models import *


class Command(BaseCommand):
    """
    Import Local Songs

    Description:
        Recursively searches provided `dir_path` for `.mp3` files. 
        Imports them with (`artist`, `album`, `title`) tags found on each file 
        or prompts user for providing (`artist`, `title`) tags if not found.

    Arguments:
        --dir_path : Directory from which files will be imported.

    Example call:
        python manage.py import_songs --dir_path "/Users/tonisredanovic/Documents/Music/mymusic"
    """

    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('--dir_path')

    def handle(self, *args, **options):
        # Config
        dir_path = options['dir_path']
        valid_extensions = ['.mp3']

        # All file paths from provided directory
        file_paths = [
            os.path.join(dp, f) for dp, dn, filenames in os.walk(dir_path) 
            for f in filenames if os.path.splitext(f)[1] in valid_extensions
        ]
        file_paths_count = len(file_paths)
        self.logger.info('Audio files found: {}'.format(file_paths_count))

        for i, file_path in enumerate(file_paths, 1):
            self.logger.info('Importing: {} ({}/{})'.format(os.path.basename(file_path), i, file_paths_count))

            # Read file
            tag = eyed3.load(file_path).tag
            file_title = tag.title
            file_artist = tag.artist
            file_album = tag.album

            # Set title and artist if not set
            tag_changed = False
            if not file_title:
                file_title = manually_set_value('title')
                tag.title = file_title
                tag_changed = True
            if not file_artist:
                file_artist = manually_set_value('artist')
                tag.artist = file_artist
                tag_changed = True
            if tag_changed:
                tag.save()
            
            with transaction.atomic():
                # Get or create artist
                artist, artist_created = Artist.objects.get_or_create(
                    name=file_artist
                    )

                # Get or create album
                if file_album:
                    album, album_created = Album.objects.get_or_create(
                        name=file_album, 
                        artist=artist
                        )
                else:
                    album = None
                
                # Get or create song
                with open(file_path, 'rb') as f:
                    song, song_created = Song.objects.get_or_create(
                        title=file_title, 
                        artist=artist, 
                        album=album,
                        defaults={
                            'source': Song.IMPORT,
                            'file': File(f, 
                            name='{} - {}{}'.format(file_artist, file_title, os.path.splitext(file_path)[1]).replace('/', ' ')
                            )
                        },
                    )
