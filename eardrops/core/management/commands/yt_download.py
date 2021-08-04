import logging
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files import File
from django.db import transaction
import eyed3

from eardrops.settings import BASE_DIR
from core.helpers import manually_set_value, confirm
from core.models import *
from core.yt_download import *



class Command(BaseCommand):
    """
    Download Youtube Songs

    Description:
        Parses a file provided with `file_path` for valid youtube URLs (skipps already downloaded URLs).
        Downloads audio from all provided URLs and fetches youtube metadata for each download. 
        Fills (`artist`, `album`, `title`) tags from metadata or prompts user for (`artist`, `title`) tags if not found, asks for confirmation on each fill.
        Shows summary of downloads and asks for confirmation before import.

    Arguments:
        --file_path : File containg links (separated by linebreaks) to youtube videos from which audio will be downloaded.

    Example call:
        python manage.py yt_download --file_path "/Users/tonisredanovic/Documents/Music/imports/YT11.txt"
    """

    logger = logging.getLogger(__name__)

    MEDIA_TEMP_ROOT = Path.joinpath(BASE_DIR, 'media_temp/')

    def add_arguments(self, parser):
        parser.add_argument('--file_path')

    def handle(self, *args, **options):
        # Config
        file_path = options['file_path']

        # Read input
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Process lines
        data_objects = process_input(lines)

        # Check for existing ids
        data_objects_new = []
        data_objects_existing = []
        existing_video_ids = list(Song.objects.exclude(youtube_id__exact='').values_list('youtube_id', flat=True))
        for data_object in data_objects:
            if data_object['video_id'] not in existing_video_ids:
                data_objects_new.append(data_object)
                existing_video_ids.append(data_object['video_id'])
            else:
                data_objects_existing.append(data_object)
        self.logger.info('Existing youtube video ids: {}'.format([data_object_existing['video_id'] for data_object_existing in data_objects_existing]))

        data_objects = data_objects_new

        # Download songs
        for data_object in data_objects:
            self.logger.info('Fetching: {}'.format(data_object['clean_url']))

            down_file_path = Path.joinpath(self.MEDIA_TEMP_ROOT, '{}.mp3'.format(data_object['video_id']))
            data_object['down_file_path'] = down_file_path

            if not os.path.exists(down_file_path):
                video_info = download_mp3(data_object['clean_url'], self.MEDIA_TEMP_ROOT)
            else:
                video_info = get_info(data_object['clean_url'])
            data_object['video_info'] = video_info

        # Process songs
        for data_object in data_objects:
            print('Data for: {}'.format(data_object['video_info']['title']))
            data_object['artist'] = manually_set_value('artist', default_value=data_object['video_info'].get('artist', None))
            data_object['track'] = manually_set_value('track', default_value=data_object['video_info'].get('track', None))
            data_object['album'] = data_object['video_info'].get('album', None)
        
        # Print summary and confirm
        print('Summary:')
        for i, data_object in enumerate(data_objects, 1):
            print('{}. | {} | {} | {}'.format(i, data_object['artist'], data_object['track'], data_object.get('album')))
        
        if not confirm('summary'):
            import pdb
            pdb.set_trace()

        # Import songs
        for data_object in data_objects:
            # Set tags
            tag = eyed3.load(data_object['down_file_path']).tag
            tag.artist = data_object['artist']
            tag.title = data_object['track']
            tag.album = data_object.get('album')
            tag.save()
            
            # Import to DB
            with transaction.atomic():
                # Get or create artist
                artist, artist_created = Artist.objects.get_or_create(
                    name=data_object['artist']
                    )

                # Get or create album
                if data_object.get('album'):
                    album, album_created = Album.objects.get_or_create(
                        name=data_object.get('album'), 
                        artist=artist
                        )
                else:
                    album = None
                
                # Get or create song
                with open(data_object['down_file_path'], 'rb') as f:
                    song, song_created = Song.objects.get_or_create(
                        title=data_object['track'], 
                        artist=artist, 
                        album=album,
                        youtube_id=data_object['video_id'],
                        defaults={
                            'source': Song.YOUTUBE,
                            'file': File(f, name='{} - {}.mp3'.format(data_object['artist'], data_object['track']).replace('/', ' ')),
                            'youtube_info': data_object['video_info']
                        },
                    )
        self.logger.info('Import done.')