from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
import urllib
from django.shortcuts import render, redirect

from ..models import *

import csv

import environ

import twitter

@permission_required('songdata.change_songnew')
def send_twitter(request):
	env = environ.Env()
	env.read_env('.env')

	# 取得したキーとアクセストークンを設定する
	auth = twitter.OAuth(consumer_key=env('TWITTER_DB_API_KEY'),
						consumer_secret=env('TWITTER_DB_API_KEY_SECRET'),
						token=env('TWITTER_DB_ACCESS_TOKEN'),
						token_secret=env('TWITTER_DB_ACCESS_TOKEN_SECRET'))

	t = twitter.Twitter(auth=auth)

	# twitterへメッセージを投稿する
	t.statuses.update(status="テスト投稿")
	return HttpResponse('twitter')

@permission_required('songdata.change_songnew')
def mail(request):
	ac = AccountAndCreatorApplication.objects.all()[0]
	username = ac.user.username
	creator = ac.creator.name
	reg_date_jst = ac.reg_date.astimezone(datetime.timezone(datetime.timedelta(hours=+9)))
	reg_date = reg_date_jst.strftime('%Y/%m/%d %H:%M:%S')
	dealing = ac.dealing

	subject = "【駅名動画DB】作者紐づけ申請"
	message = "作者紐づけの申請を受信しました。\n\n--------\nユーザー名：" + username + "\n作者：" + creator + "\n日時：" + reg_date + "\n動画の扱い：" + dealing + "\n--------\n\n駅名動画データベース STANMIC DATABASE stanmic.com\n© 2022 nignagIC"
	
	from_email = "stanmic.database@gmail.com"
	recipient_list = ["icnignag@gmail.com"]

	send_mail(subject, message, from_email, recipient_list)
	return HttpResponse('send')

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
