from django.contrib import admin
from .models import *

class SongNewAdmin(admin.ModelAdmin):
	list_display = ('song_name', 'song_name_kana', 'artist_name', 'artist_name_kana')
	search_fields = ('song_name',)

class VocalNewAdmin(admin.ModelAdmin):
	list_display = ('name', 'name_kana')

# Register your models here.
# admin.site.register(Artist, ArtistAdmin)
# admin.site.register(Song, SongAdmin)
admin.site.register(SongNew, SongNewAdmin)
admin.site.register(VocalNew, VocalNewAdmin)