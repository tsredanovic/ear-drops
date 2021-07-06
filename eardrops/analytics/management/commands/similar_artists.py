import logging

import Levenshtein
from django.core.management.base import BaseCommand

from core.models import *


class Command(BaseCommand):
    """
    Find similar artists

    Description:
        Finds all pairs of artists whose names have similarity (Levenshtein distance) above defined threshold.

    Arguments:
        --threshold : Similarity detection threshold - only pairs with similarity above will be detected

    Example call:
        python manage.py similarity --threshold 0.7
    """

    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('--threshold')

    def handle(self, *args, **options):
        # Config
        threshold = float(options['threshold'])

        # Get artists
        artists = list(Artist.objects.order_by('name').values('id', 'name'))
        artists_count = len(artists)

        # Find similar artists
        similars = []
        for i in range(artists_count):
            for j in range(i+1, artists_count):
                # Detect similarity
                similarity = Levenshtein.ratio(artists[i]['name'], artists[j]['name'])
                if similarity >= threshold:
                    similars.append({'artist1': artists[i]['name'], 'artist2': artists[j]['name'], 'similarity': similarity})

        # Sort by similarity
        similars = sorted(similars, key=lambda k: k['similarity'], reverse=True) 

        # Report
        for similar_pair in similars:
            self.logger.info('{} - {}: {:.2f}'.format(similar_pair['artist1'], similar_pair['artist2'], similar_pair['similarity']))
