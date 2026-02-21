import datetime
import re
import pytz

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import serializer

from ..models import *

def _today_movies():
	now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
	return Movie.objects.filter(published_at_month=now.month, published_at_day=now.day)

def _serialize_movie(movie):
	if not movie:
		return None

	published_at = movie.published_at.astimezone(pytz.timezone('Asia/Tokyo')) if movie.published_at else None
	return {
		'main_id': movie.main_id,
		'title': movie.title,
		'youtube_id': movie.youtube_id,
		'published_at': published_at.isoformat() if published_at else None,
		'published_at_text': published_at.strftime('%Y/%m/%d') if published_at else '',
		'is_collab': movie.get_is_collab_display(),
		'categories': movie.category(),
		'channel': movie.channel.name if movie.channel else '',
		'duration': movie.get_duration() if movie.duration else '',
		'detail_url': reverse('moviedatabase:detail', kwargs={'main_id': movie.main_id}),
	}

class TopPageViewSet(APIView):
	def get(self, request):
		movies = Movie.objects.all().exclude(is_active=False)[:6]
		update_list = MovieUpdateInformation.objects.all()[:10]
		notice_list = NoticeInformation.objects.all()[:10]
		top_img = TopImage.objects.all().order_by('?').first()
		today_movie = _today_movies().order_by('?').first()

		def to_jst_text(value):
			if not value:
				return ''
			return timezone.localtime(value, pytz.timezone('Asia/Tokyo')).strftime('%Y/%m/%d')

		payload = {
			'today_text': timezone.localtime(timezone.now(), pytz.timezone('Asia/Tokyo')).strftime('%m/%d'),
			'top_image_url': f"{settings.STATIC_URL}moviedatabase/img-top/{top_img.file_name}" if top_img and top_img.file_name else '',
			'movies': [_serialize_movie(movie) for movie in movies],
			'today_movie': _serialize_movie(today_movie),
			'notices': [
				{
					'id': info.pk,
					'reg_date': to_jst_text(info.reg_date),
					'category': info.category or '',
					'head': info.head or '',
					'url': reverse('moviedatabase:notice', kwargs={'pk': info.pk}),
				}
				for info in notice_list
			],
			'updates': [
				{
					'reg_date': to_jst_text(info.reg_date),
					'label': f"動画{info.get_is_create_display()}" if info.movie else f"製作者{info.get_is_create_display()}",
					'text': info.text(),
					'url': reverse('moviedatabase:detail', kwargs={'main_id': info.movie.main_id}) if info.movie else (
						reverse('moviedatabase:movielistbycreator', kwargs={'creator': info.creator.pk}) if info.creator else ''
					),
				}
				for info in update_list
			],
		}
		return Response(payload)

class StationServicebyLineServiceViewSet(generics.ListAPIView):
	serializer_class = serializer.StationServiceSerializer
	def get_queryset(self):
		q = self.kwargs['line_service']
		return StationService.objects.filter(line_service=q).order_by('sort_by_line_service')

class StationbyLineViewSet(generics.ListAPIView):
	serializer_class = serializer.StationSerializer
	def get_queryset(self):
		q = self.kwargs['line']
		return Station.objects.filter(line=q).order_by('sort_by_line')

class LineServicebyPrefectureViewSet(generics.ListAPIView):
	serializer_class = serializer.LineServiceSerializer
	def get_queryset(self):
		q = self.kwargs['pref']
		return LineService.objects.filter(prefs__id=q)

class LineServicebyCompanyViewSet(generics.ListAPIView):
	serializer_class = serializer.LineServiceSerializer
	def get_queryset(self):
		q = self.kwargs['company']
		return LineService.objects.filter(company__id=q)
        
class StationServiceWithLineSearchViewSet(generics.ListAPIView):
	serializer_class = serializer.StationServiceSerializer
	def get_queryset(self):
		result = searchStationService(self.kwargs['station'], self.kwargs['line'])

		return duplicate_delection(result)

class StationServiceSearchViewSet(generics.ListAPIView):
	serializer_class = serializer.StationServiceSerializer
	def get_queryset(self):
		if (self.request.GET.get('exact')):
			result = searchStationService(self.kwargs['station'], "")
		else:
			s = text_normalization(self.kwargs['station'])
			result = StationService.objects.filter(name__contains=s)

		return duplicate_delection(result)
		return result

class GroupStationSearchViewSet(generics.ListAPIView):
	serializer_class = serializer.StationSerializer
	def get_queryset(self):
		q = self.kwargs['word']
		ss = Station.objects.filter(name__contains=q)
		c = Station.objects.none()
		for s in ss:
			if s.group_station_new:
				c |= Station.objects.filter(pk=s.group_station_new.id)
		return c

class LineServiceTransferViewSet(generics.ListAPIView):
	serializer_class = serializer.LineServiceSerializer
	def get_queryset(self):
		stationservice = StationService.objects.get(pk=self.kwargs['station_service'])
		stations = stationservice.station.get_group_station()
		lineservices = LineService.objects.none()
		for station in stations:
			stationservices = StationService.objects.filter(station=station)
			for stationservice in stationservices:
				lineservices |= LineService.objects.filter(pk=stationservice.line_service.pk)
		return lineservices

class PartStationViewSet(generics.ListAPIView):
	serializer_class = serializer.StationInMovieSerializer
	def get_queryset(self):
		return StationInMovie.objects.filter(part=self.kwargs['id']).order_by('sort_by_part')

class MoviebyChannelViewSet(generics.ListAPIView):
	serializer_class = serializer.MovieSerializer
	def get_queryset(self):
		return Movie.objects.filter(channel=self.kwargs['channel']).order_by('-published_at')

class MovieViewSet(generics.ListAPIView):
	serializer_class = serializer.MovieSerializer
	def get_queryset(self):
		return Movie.objects.filter(id=self.kwargs['movie'])

class NamebyCreatorViewSet(generics.ListAPIView):
	serializer_class = serializer.NameSerializer
	def get_queryset(self):
		return Name.objects.filter(creator=self.kwargs['creator'])

class NameViewSet(generics.ListAPIView):
	serializer_class = serializer.NameSerializer
	def get_queryset(self):
		return Name.objects.filter(id=self.kwargs['name'])

class MovieIsExistViewSet(generics.ListAPIView):
	serializer_class = serializer.MovieIsExistSerializer
	def get_queryset(self):
		return Movie.objects.filter(main_id=self.kwargs['main_id'])
        

hyphen = "-˗֊‐‑‒–⁃⁻₋−"
prolonged_sound_mark = "ー—―─━ｰ"
middle_dot = "·ᐧ•∙⋅⸱・･"
parentheses = "【(『「[<《{≪〈〔（＜［｛｟"
parentheses_end = "】)』」]>》}≫〉〕）＞］｝｠"

def text_normalization(s):
	s = re.sub(r"\<.+?\>", "|", s)
	s = s.replace(' ', '|')
	for h in hyphen:
		s = s.replace(h, '|')
	for p in prolonged_sound_mark:
		s = s.replace(p, 'ー')
	for m in middle_dot:
		s = s.replace(m, '・')
	for p in parentheses:
		s = s.replace(p, '|')
	for e in parentheses_end:
		s = s.replace(e, '|')
	return s

def search_pref(text_array):
	for text in text_array:
		if (len(text) < 2):
			continue
		pref_q = Prefecture.objects.filter(name__contains=text)
		if (pref_q.count() != 0):
			return text

	return ""

def get_kata_ngram(string, mode=0):
    """
    入力された文字列を最大数としたn-gramの出力
    @text: ngramを取得する文字列
    """
    srt_len = len(string) + 1
    result = []
    for n in range(1, srt_len):
        result.append([string[k:k+n]
                        for k in range(len(string)-n+1)])
    return result[::-1]

def searchStationService(q1, q2):
	q1 = text_normalization(q1).split('|')
	s = ""
	for sp in q1:
		if (sp != ""):
			s = sp
			break
	pref = search_pref(q1)

	q2 = text_normalization(q2).split('|')

	for litem in reversed(q2):
		for ll in get_kata_ngram(litem):
			for l in ll:
				stations = StationService.objects.filter(name=s, line_service__name__icontains=l, station__pref__name__icontains=pref)
				if (stations.count() != 0):
					return stations

				stations = StationService.objects.filter(name__contains=s, line_service__name__icontains=l, station__pref__name__icontains=pref)
				if (stations.count() != 0):
					return stations

				stations = StationService.objects.filter(name__contains=s, station__line__name__icontains=l, station__pref__name__icontains=pref)
				if (stations.count() != 0):
					return stations

	for litem in q2:
		for ll in get_kata_ngram(litem):
			for l in ll:
				stations = StationService.objects.filter(name=s, line_service__company__name__icontains=l, station__pref__name__icontains=pref)
				if (stations.count() != 0):
					return stations

				stations = StationService.objects.filter(name__contains=s, line_service__company__name__icontains=l)
				if (stations.count() != 0):
					return stations

	for sitem in reversed(q1):
		for ss in get_kata_ngram(sitem):
			for s in ss:
				stations = StationService.objects.filter(name=s)
				if (stations.count() != 0):
					return stations

				stations = StationService.objects.filter(name__contains=s)
				if (stations.count() != 0):
					return stations

	return StationService.objects.none()

def duplicate_delection(result):
	query = StationService.objects.none()
	for r in result:
		if ((r.prev_group() != r.next_group()) and (r.prev_group().station.line == r.next_group().station.line)):
			if (r.prev_group() == r):
				query |= StationService.objects.filter(pk=r.pk)
		else:
			query |= StationService.objects.filter(pk=r.pk)

	return query
