import logging
from pathlib import Path

from django.core.management.base import BaseCommand
import eyed3

from eardrops.settings import MEDIA_ROOT
from core.helpers import manually_set_value, confirm
from core.models import *


class Command(BaseCommand):
    """
    Edit song's tags

    Description:
        Prompts user for (`artist`, `album`, `title`) to edit exiting song.

    Arguments:
        --song_id : ID of a song to edit.

    Example call:
        python manage.py edit_song --song_id 665
    """

    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('--song_id')

    def handle(self, *args, **options):
        # Config
        song_id = options['song_id']

        # Fetch song
        song = Song.objects.get(id=song_id)
        self.logger.info('Editing song: {}\n\tArtist: {}\n\tTitle: {}\n\tAlbum: {}'.format(song.file, song.artist.name, song.title, song.album.name))

        # Input new data
        new_artist_name = manually_set_value('artist', default_value=song.artist.name)
        new_title = manually_set_value('title', default_value=song.title)
        new_album_name = manually_set_value('album', default_value=song.album.name)

        # Confirm new data
        print('New song data:\n\tArtist: {}\n\tTitle: {}\n\tAlbum: {}'.format(new_artist_name, new_title, new_album_name))
        if not confirm('new data'):
            import pdb
            pdb.set_trace()

        # Save new values
        is_changed = False
        tag = eyed3.load(song.file.path).tag

        if new_artist_name != song.artist.name if song.artist else None:
            old_artist = song.artist
            new_artist, artist_created = Artist.objects.get_or_create(
                name=new_artist_name
                )
            song.artist = new_artist
            tag.artist = new_artist.name
            if not old_artist.songs.exists():
                old_artist.delete()
            is_changed = True
            self.logger.info('Artist updated.')


        if new_album_name != song.album.name if song.album else '':
            old_album = song.album
            new_album, album_created = Album.objects.get_or_create(
                name=new_album_name, 
                artist=new_artist
                )
            song.album = new_album
            tag.album = new_album.name
            if not old_album.songs.exists():
                old_album.delete()
            is_changed = True
            self.logger.info('Album updated.')
            
        if new_title != song.title:
            song.title = new_title
            tag.title = new_title
            is_changed = True
            self.logger.info('Title updated.')
        
        if not is_changed:
            self.logger.info('No changes detected. Exiting.')
            return
        
        new_file_name = '{} - {}.mp3'.format(new_artist_name, new_title).replace('/', ' ')
        new_file_path = Path.joinpath(MEDIA_ROOT, 'songs/', new_file_name)
        os.rename(song.file.path, new_file_path)
        song.file.name = 'songs/{}'.format(new_file_name)
        song.save()
        tag.save()
        self.logger.info('Song updated.')
