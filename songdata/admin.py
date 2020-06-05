from django.contrib import admin
from .models import *

class SongAdmin(admin.ModelAdmin):
	list_display = ('name', 'name_kana')

class ArtistAdmin(admin.ModelAdmin):
	list_display = ('name', 'name_kana')

# Register your models here.
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(VocalNew)