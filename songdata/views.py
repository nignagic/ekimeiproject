from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from django.contrib.auth.decorators import permission_required

from rest_framework import generics
from .models import *
from . import serializer

# Create your views here.
class SongCreate(PermissionRequiredMixin, generic.CreateView):
	model = Song
	fields = '__all__'
	permission_required = ('songdata.add_song')
	success_url = reverse_lazy('songdata:songlist')

class PopupSongCreate(SongCreate):
	def form_valid(self, form):
		song = form.save()
		artist = ""
		songs = song.artist.all()
		for s in song.artist.all():
			artist = artist + s.name + " "
		context = {
			'object_name': str(song),
			'object_pk': song.pk,
			'object_artist': artist,
			'function_name': 'add_song'
		}
		return render(self.request, 'songdata/close_song.html', context)

class SongNewCreate(PermissionRequiredMixin, generic.CreateView):
	model = SongNew
	fields = '__all__'
	permission_required = ('songdata.add_songnew')
	success_url = reverse_lazy('songdata:songlist')

class PopupSongNewCreate(SongNewCreate):
	def form_valid(self, form):
		songnew = form.save()
		songnew.user = self.request.user
		songnew.save()
		context = {
			'object_name': str(songnew),
			'object_pk': songnew.pk,
			'function_name': 'add_songnew'
		}
		return render(self.request, 'songdata/close_songnew.html', context)

class ArtistCreate(PermissionRequiredMixin, generic.CreateView):
	model = Artist
	fields = '__all__'
	permission_required = ('songdata.add_artist')
	success_url = reverse_lazy('songdata:artistlist')

class PopupArtistCreate(ArtistCreate):
	def form_valid(self, form):
		return self
		artist = form.save()
		context = {
			'object_name': str(artist),
			'object_pk': artist.pk,
			'object_initial': artist.initial,
			'function_name': 'add_artist'
		}
		return render(self.request, 'songdata/close_artist.html', context)

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

@permission_required('songdata.add_songnew')
def popup_song_setting(request):
	if request.method == 'POST':

		context = {
			'song_list': request.POST['selected-song-list']
		}
		return render(request, 'songdata/close_song_setting.html', context)

	songnews = SongNew.objects.all()

	context = {
		'songnews': songnews,
	}

	return render(request, 'songdata/song_setting.html', context)

@permission_required('songdata.add_vocalnew')
def popup_vocal_setting(request):
	if request.method == 'POST':

		context = {
			'vocal_list': request.POST['selected-vocal-list']
		}
		return render(request, 'songdata/close_vocal_setting.html', context)

	vocals = VocalNew.objects.all()

	context = {
		'vocals': vocals,
	}

	return render(request, 'songdata/vocal_setting.html', context)

class SongbyArtistViewSet(generics.ListAPIView):
	serializer_class = serializer.SongSerializer
	def get_queryset(self):
		return Song.objects.filter(artist=self.kwargs['artist'])

class SongViewSet(generics.ListAPIView):
	serializer_class = serializer.SongSerializer
	def get_queryset(self):
		return Song.objects.filter(pk=self.kwargs['song'])

class SongNewViewSet(generics.ListAPIView):
	serializer_class = serializer.SongNewSerializer
	def get_queryset(self):
		return SongNew.objects.filter(pk=self.kwargs['songnew'])

class VocalViewSet(generics.ListAPIView):
	serializer_class = serializer.VocalNewSerializer
	def get_queryset(self):
		return VocalNew.objects.filter(pk=self.kwargs['vocal'])