from rest_framework import generics
from .. import serializer

from ..models import *

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
	s = re.sub("\<.+?\>", "|", s)
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