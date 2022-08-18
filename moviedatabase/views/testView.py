from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
import urllib
from django.shortcuts import render

from ..models import *

import csv

@permission_required('songdata.change_songnew')
def test(request):
	response = HttpResponse(content_type='text/csv')
	filename = urllib.parse.quote((u'曲一覧.csv').encode("utf8"))
	response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
	writer = csv.writer(response)
	prev = None

	for song in SongNew.objects.all():
		if (song.song_name == None):
			song.song_name = ''
		if (song.song_name_kana == None):
			song.song_name_kana = ''
		if (song.artist_name == None):
			song.artist_name = ''
		if (song.artist_name_kana == None):
			song.artist_name_kana = ''
		if (song.tag == None):
			song.tag = ''
		song.save()

	for song in SongNew.objects.all():
		same_songs = SongNew.objects.filter(song_name=song.song_name, song_name_kana=song.song_name_kana, artist_name=song.artist_name, artist_name_kana=song.artist_name_kana, tag=song.tag)
		same_song_first = same_songs.order_by('pk').first()
		for same_song in same_songs:
			for m in same_song.movie_set.all():
				m.songnew.remove(same_song)
				m.songnew.add(same_song_first)
			for p in same_song.part_set.all():
				p.songnew.remove(same_song)
				p.songnew.add(same_song_first)

	for song in SongNew.objects.all():
		movie_count = song.movie_set.all().count()
		part_count = song.part_set.all().count()
		if (movie_count == 0 and part_count == 0):
			song.delete()

	for song in SongNew.objects.all():
		same_songs = SongNew.objects.filter(song_name=song.song_name, song_name_kana=song.song_name_kana, artist_name=song.artist_name, artist_name_kana=song.artist_name_kana, tag=song.tag)
		writer.writerow([song.song_name, song.song_name_kana, song.artist_name, song.artist_name_kana, song.tag, same_songs.count()])

	return response

@permission_required('moviedatabase.add_stationinmovie')
def MultipleStationUpload(request):

	context = {
	}

	return render(request, 'moviedatabase/multiple_station_upload.html', context)

@permission_required('moviedatabase.add_stationinmovie')
def MultipleStationSearch(request):
	if request.method == 'POST':
		station_line_list = request.POST['station-line-list']
		station_text = ""
		line_text = ""
		for station_line in station_line_list.splitlines():
			sl = station_line.split('\t', 1);
			station_text = station_text + sl[0] + "\n"
			line_text = line_text + sl[1] + "\n"
			
		context = {
			'station_text': station_text,
			'line_text': line_text
		}

		return render(request, 'moviedatabase/multiple_station_search.html', context)

	context = {
	}

	return render(request, 'moviedatabase/multiple_station_search.html', context)
