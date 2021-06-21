from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from core.models import *


class SongAdmin(admin.ModelAdmin):
    model = Song

    list_display = ('artist', 'title', 'album', 'file', 'source', 'created_at', 'updated_at', )
    list_display_links = ('title', )
    list_filter = ('source', )
    search_fields = ('title', 'artist', 'album')
    ordering = ('-artist', '-title')


class ArtistAdmin(admin.ModelAdmin):
    model = Artist

    list_display = ('name', 'songs_list', 'albums_list', 'created_at', 'updated_at', )
    list_display_links = ('name', )
    search_fields = ('name', )
    ordering = ('-name', )

    @admin.display(description='Songs')
    def songs_list(self, instance):
        return format_html_join(
            mark_safe('<br>'),
            '{}',
            ((line,) for line in [song_title for song_title in instance.songs.order_by('title').values_list('title', flat=True)]),
        ) or mark_safe("<span class='errors'>No songs.</span>")
    
    @admin.display(description='Albums')
    def albums_list(self, instance):
        return format_html_join(
            mark_safe('<br>'),
            '{}',
            ((line,) for line in [album_name for album_name in instance.albums.order_by('name').values_list('name', flat=True)]),
        ) or mark_safe("<span class='errors'>No albums.</span>")


class AlbumAdmin(admin.ModelAdmin):
    model = Album

    list_display = ('name', 'artist', 'songs_list', 'created_at', 'updated_at', )
    list_display_links = ('name', )
    search_fields = ('name', )
    ordering = ('-name', )

    @admin.display(description='Songs')
    def songs_list(self, instance):
        return format_html_join(
            mark_safe('<br>'),
            '{}',
            ((line,) for line in [song_title for song_title in instance.songs.order_by('title').values_list('title', flat=True)]),
        ) or mark_safe("<span class='errors'>No songs.</span>")


admin.site.register(Song, SongAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)