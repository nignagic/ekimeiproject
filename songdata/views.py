from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from .models import *

# Create your views here.
class SongCreate(PermissionRequiredMixin, generic.CreateView):
	model = Song
	fields = '__all__'
	permission_required = ('songdata.add_song')
	success_url = reverse_lazy('songdata:songlist')

class PopupSongCreate(SongCreate):
	def form_valid(self, form):
		song = form.save()
		context = {
			'object_name': str(song),
			'object_pk': song.pk,
			'function_name': 'add_song'
		}
		return render(self.request, 'songdata/close.html', context)

class ArtistCreate(PermissionRequiredMixin, generic.CreateView):
	model = Artist
	fields = '__all__'
	permission_required = ('songdata.add_artist')
	success_url = reverse_lazy('songdata:artistlist')

class PopupArtistCreate(ArtistCreate):
	def form_valid(self, form):
		artist = form.save()
		context = {
			'object_name': str(artist),
			'object_pk': artist.pk,
			'function_name': 'add_artist'
		}
		return render(self.request, 'songdata/close.html', context)

class VocalCreate(PermissionRequiredMixin, generic.CreateView):
	model = VocalNew
	fields = '__all__'
	permission_required = ('songdata.add_vocalnew')
	success_url = reverse_lazy('songdata:vocallist')

class PopupVocalCreate(VocalCreate):
	def form_valid(self, form):
		vocal = form.save()
		context = {
			'object_name': str(vocal),
			'object_pk': vocal.pk,
			'function_name': 'add_vocalnew'
		}
		return render(self.request, 'songdata/close.html', context)