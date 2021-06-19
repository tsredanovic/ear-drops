from django.contrib import admin

from core.models import Song


class SongAdmin(admin.ModelAdmin):
    model = Song

    list_display = ('artist', 'title', 'album', 'file', 'source')
    list_display_links = ('title', )
    list_filter = ('source', )
    search_fields = ('title', 'artist', 'album')
    ordering = ('-artist', '-title')


admin.site.register(Song, SongAdmin)