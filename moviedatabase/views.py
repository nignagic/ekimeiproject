from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone
from rest_framework import generics
from . import serializer
from django.db.models import Q

from .models import *
from stationdata.models import *
from songdata.models import *

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import (
	LoginView, LogoutView
)
from . import forms
from django.contrib.auth.decorators import permission_required

import datetime

# Create your views here.
class Top(generic.ListView):
	model = Movie
	template_name = 'moviedatabase/top.html'

	def get_context_data(self):
		movies = Movie.objects.all().order_by('-published_at')[:6]
		update_list = MovieUpdateInformation.objects.all()
		notice_list = NoticeInformation.objects.all()
		context = {
			'movie_list': movies,
			'update_list': update_list,
			'notice_list': notice_list
		}

		return context

class Login(LoginView):
	form_class = forms.LoginForm
	template_name = 'moviedatabase/login.html'

class Logout(LogoutView):
	template_name = 'moviedatabase/logout.html'

def Mypage(request):
	updateinformations = MovieUpdateInformation.objects.filter(user=request.user)

	context = {
		'updateinformations': updateinformations,
		'user': request.user
	}

	return render(request, 'moviedatabase/mypage.html', context)

def Terms(request):
	return render(request, 'moviedatabase/static-page/terms.html')


class MovieListView(generic.ListView):
	model = Movie
	template_name = 'moviedatabase/movielist.html'
	queryset = Movie.objects.all()
	paginate_by = 12
	ordering = '-published_at'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		word = self.request.GET.get('word')
		if word:
			parts = Part.objects.filter(Q(name__icontains=word) | Q(explanation__icontains=word))
			for part in parts:
				queryset |= Movie.objects.filter(pk=part.movie.pk)
			queryset |= Movie.objects.filter(Q(title__icontains=word) | Q(main_id__icontains=word) | Q(description__icontains=word) | Q(explanation__icontains=word))
		else:
			queryset = Movie.objects.all()
		return queryset.order_by('-published_at')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		word = self.request.GET.get('word')
		context['word'] = word

		queryset = Movie.objects.none()
		if word:
			parts = Part.objects.filter(Q(name__icontains=word) | Q(explanation__icontains=word))
			for part in parts:
				queryset |= Movie.objects.filter(pk=part.movie.pk)
			queryset |= Movie.objects.filter(Q(title__icontains=word) | Q(main_id__icontains=word) | Q(description__icontains=word) | Q(explanation__icontains=word))
		else:
			queryset = Movie.objects.all()
		
		context['count'] = queryset.count()

		return context

def FreeSearchView(request):
	word = request.GET.get('word')

	movies = Movie.objects.none()
	if word:
		parts = Part.objects.filter(Q(name__icontains=word) | Q(explanation__icontains=word))
		for part in parts:
			movies |= Movie.objects.filter(pk=part.movie.pk)
		movies |= Movie.objects.filter(Q(title__icontains=word) | Q(main_id__icontains=word) | Q(description__icontains=word) | Q(explanation__icontains=word))
	mcount = movies.count
	movies = movies.order_by('-published_at')[:5]

	lineservices = LineService.objects.none()
	if word:
		lineservices = LineService.objects.filter(Q(name__icontains=word) | Q(name_sub__icontains=word)).order_by('company', 'sort_by_company')
	lcount = lineservices.count
	lineservices = lineservices[:10]

	stationservices = StationService.objects.none()
	if word:
		stationservices = StationService.objects.filter(name__icontains=word).order_by('line_service')
	scount = stationservices.count
	stationservices = stationservices[:10]

	creators = Creator.objects.none()
	if word:
		creators = Creator.objects.filter(Q(name__icontains=word) | Q(name_kana__icontains=word)).order_by('name_kana')
	ccount = creators.count
	creators = creators[:10]

	movies_artist = Movie.objects.none()
	if word:
		songnews = SongNew.objects.filter(Q(artist_name__icontains=word) | Q(artist_name_kana__icontains=word)).order_by('artist_name_kana')
		for song in songnews:
			movies_artist |= Movie.objects.filter(songnew=song)
			parts = Part.objects.filter(songnew=song)
			for part in parts:
				movies_artist |= Movie.objects.filter(pk=part.movie.pk)
	
	movies_artist = movies_artist.exclude(is_active=False).order_by('-published_at').distinct()
	acount = movies_artist.count
	movies_artist = moviequery(movies_artist, "pub", "n")[:5]

	movies_song = Movie.objects.none()
	if word:
		songnews = SongNew.objects.filter(Q(song_name__icontains=word) | Q(song_name_kana__icontains=word) | Q(tag__icontains=word)).order_by('song_name_kana')
		for song in songnews:
			movies_song |= Movie.objects.filter(songnew=song)
			parts = Part.objects.filter(songnew=song)
			for part in parts:
				movies_song |= Movie.objects.filter(pk=part.movie.pk)
	
	movies_song = movies_song.exclude(is_active=False).order_by('-published_at').distinct()
	songcount = movies_song.count
	movies_song = moviequery(movies_song, "pub", "n")[:5]

	context = {
		'movie_list': movies,
		"lineservices": lineservices,
		"stationservices": stationservices,
		"creators": creators,
		"movies_artist": movies_artist,
		"movies_song": movies_song,
		'mcount': mcount,
		'lcount': lcount,
		'scount': scount,
		'ccount': ccount,
		'acount': acount,
		'songcount': songcount,
		"word": word
	}

	return render(request, 'moviedatabase/freesearch.html', context)

class RailwayTopView(generic.TemplateView):
	template_name = 'moviedatabase/railway/railwaytop.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['regions'] = Region.objects.filter(country__name__contains="日本")
		context['countries'] = Country.objects.all()
		context['categories'] = BelongsCategory.objects.all()[:20]

		return context

class BelongsCategoryListView(generic.ListView):
	model = BelongsCategory
	paginate_by = 30
	queryset = BelongsCategory.objects.all()
	template_name = 'moviedatabase/railway/categorylist.html'

class LineServiceListbyCountryView(generic.ListView):
	model = LineService
	paginate_by = 30
	template_name = 'moviedatabase/railway/lineservicelistbycountry.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = LineService.objects.none()
		country = Country.objects.get(pk=self.kwargs['country'])
		prefs = Prefecture.objects.filter(region__country=country)
		for pref in prefs:
			queryset |= LineService.objects.filter(prefs=pref)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		country = Country.objects.get(pk=self.kwargs['country'])

		queryset = LineService.objects.none()
		country = Country.objects.get(pk=self.kwargs['country'])
		prefs = Prefecture.objects.filter(region__country=country)
		for pref in prefs:
			queryset |= LineService.objects.filter(prefs=pref)
		companies = Company.objects.none()
		for q in queryset:
			companies |= Company.objects.filter(pk=q.company.pk)

		context['country'] = country
		context['companies'] = companies

		return context

class CompanyListbyRegionView(generic.ListView):
	model = Company
	paginate_by = 30
	template_name = 'moviedatabase/railway/companylistbyregion.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Company.objects.none()
		region = Region.objects.get(pk=self.kwargs['region'])
		prefs = Prefecture.objects.filter(region=region)

		if self.kwargs['category'] != "all":
			category = BelongsCategory.objects.get(pk=self.kwargs['category'])
			for pref in prefs:
				lineservices = LineService.objects.filter(prefs=pref).filter(category=category)
				for lineservice in lineservices:
					queryset |= Company.objects.filter(pk=lineservice.company.pk)
		else:
			for pref in prefs:
				lineservices = LineService.objects.filter(prefs=pref)
				for lineservice in lineservices:
					queryset |= Company.objects.filter(pk=lineservice.company.pk)

		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		region = Region.objects.get(pk=self.kwargs['region'])
		prefs = Prefecture.objects.filter(region=region)

		context['region'] = region
		context['prefs'] = prefs
		if self.kwargs['category'] == "all":
			context['category'] = "すべて"
		else:
			context['category'] = BelongsCategory.objects.get(pk=self.kwargs['category'])
		context['categories'] = BelongsCategory.objects.all()[:20]

		return context

class LineServiceListbyPrefectureView(generic.ListView):
	model = LineService
	paginate_by = 30
	template_name = 'moviedatabase/railway/lineservicelistbyprefecture.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = LineService.objects.none()
		pref = Prefecture.objects.get(pk=self.kwargs['pref'])
		queryset = LineService.objects.filter(prefs=pref).order_by('company', 'sort_by_company')
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		pref = Prefecture.objects.get(pk=self.kwargs['pref'])

		qs = LineService.objects.filter(prefs=pref).order_by('company')
		companies = Company.objects.none()
		for q in qs:
			companies |= Company.objects.filter(pk=q.company.pk)

		context['pref'] = pref
		context['companies'] = companies

		return context

class LineServiceListbyCompanyView(generic.ListView):
	model = LineService
	paginate_by = 30
	template_name = 'moviedatabase/railway/lineservicelistbycompany.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = LineService.objects.none()
		company = Company.objects.get(pk=self.kwargs['company'])
		queryset = LineService.objects.filter(company=company).order_by('sort_by_company')
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		company = Company.objects.get(pk=self.kwargs['company'])

		qs = LineService.objects.filter(company=company).order_by('sort_by_company')
		prefs = Prefecture.objects.none()
		for q in qs:
			for p in q.prefs.all():
				prefs |= Prefecture.objects.filter(pk=p.pk)

		context['company'] = company
		context['prefs'] = prefs

		context['admin'] = self.request.user.groups.filter(name='admin').exists()

		return context

class LineServiceListbyCompanyandPrefectureView(generic.ListView):
	model = LineService
	paginate_by = 30
	template_name = 'moviedatabase/railway/lineservicelistbycompanyandprefecture.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = LineService.objects.none()
		company = Company.objects.get(pk=self.kwargs['company'])
		pref = Prefecture.objects.get(pk=self.kwargs['pref'])
		queryset = LineService.objects.filter(company=company).filter(prefs=pref).order_by('sort_by_company')
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		company = Company.objects.get(pk=self.kwargs['company'])
		pref = Prefecture.objects.get(pk=self.kwargs['pref'])

		context['company'] = company
		context['pref'] = pref

		return context

class LineServiceListbyCategoryView(generic.ListView):
	model = LineService
	paginate_by = 30
	template_name = 'moviedatabase/railway/lineservicelistbycategory.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = LineService.objects.none()
		category = BelongsCategory.objects.get(pk=self.kwargs['category'])
		queryset = LineService.objects.filter(category=category).order_by('company', 'sort_by_company')
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		category = BelongsCategory.objects.get(pk=self.kwargs['category'])

		context['category'] = category
		context['japan_regions'] = Region.objects.filter(country__name__contains="日本")
		context['foreign_regions'] = Region.objects.exclude(country__name__contains="日本")

		return context

class LineServiceListbyCategoryandPrefectureView(generic.ListView):
	model = LineService
	paginate_by = 30
	template_name = 'moviedatabase/railway/lineservicelistbycategoryandprefecture.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = LineService.objects.none()
		category = BelongsCategory.objects.get(pk=self.kwargs['category'])
		pref = Prefecture.objects.get(pk=self.kwargs['pref'])
		queryset = LineService.objects.filter(category=category).filter(prefs=pref).order_by('company', 'sort_by_company')
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		category = BelongsCategory.objects.get(pk=self.kwargs['category'])
		pref = Prefecture.objects.get(pk=self.kwargs['pref'])

		context['category'] = category
		context['pref'] = pref

		return context

class LineServiceSearchView(generic.ListView):
	model = LineService
	paginate_by = 30
	template_name = 'moviedatabase/railway/lineservicesearch.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = LineService.objects.none()
		word = self.request.GET.get('word')
		if word:
			queryset = LineService.objects.filter(Q(name__icontains=word) | Q(name_sub__icontains=word)).order_by('company', 'sort_by_company')
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		word = self.request.GET.get('word')
		context['word'] = word
		count = 0
		if word:
			count = LineService.objects.filter(Q(name__icontains=word) | Q(name_sub__icontains=word)).order_by('company').count()

		context['count'] = count

		return context

class StationServiceSearchView(generic.ListView):
	model = StationService
	paginate_by = 30
	template_name = 'moviedatabase/railway/stationservicesearch.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = StationService.objects.none()
		word = self.request.GET.get('word')
		if word:
			queryset = StationService.objects.filter(name__icontains=word).order_by('line_service')
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		word = self.request.GET.get('word')
		context['word'] = word
		count = 0
		if word:
			count = StationService.objects.filter(name__icontains=word).order_by('line_service').count()

		context['count'] = count

		return context

def moviequery(q, sort, order):
	if sort == "pub":
		if order == "o":
			q = q.order_by('published_at')
	elif sort == "view":
		if order == "x":
			q = q.order_by('-n_view')
		elif order == "n":
			q = q.order_by('n_view')
	return q

class MovieListbyLineView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/railway/movielistbyline.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		line = Line.objects.get(pk=self.kwargs['line'])
		stations = Station.objects.filter(line=line).order_by('sort_by_line')
		for station in stations:
			stationservices = StationService.objects.filter(station=station)
			for stationservice in stationservices:
				stationinmovies = StationInMovie.objects.filter(station_service=stationservice)
				for stationinmovie in stationinmovies:
					if (stationinmovie.part):
						queryset |= Movie.objects.filter(pk=stationinmovie.part.movie.pk)
			
		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		line = Line.objects.get(pk=self.kwargs['line'])
		stations = Station.objects.filter(line=line).order_by('sort_by_line')
		lineservices = LineService.objects.none()
		for station in stations:
			stationservices = StationService.objects.filter(station=station)
			for stationservice in stationservices:
				lineservices |= LineService.objects.filter(pk=stationservice.line_service.pk)

		context['line'] = line
		context['stations'] = stations
		context['lineservices'] = lineservices

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']

		context['admin'] = self.request.user.groups.filter(name='admin').exists()

		return context

class MovieListbyStationView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/railway/movielistbystation.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		station = Station.objects.get(pk=self.kwargs['station'])
		stationservices = StationService.objects.filter(station=station)
		for stationservice in stationservices:
			stationinmovies = StationInMovie.objects.filter(station_service=stationservice)
			for stationinmovie in stationinmovies:
				if (stationinmovie.part):
					queryset |= Movie.objects.filter(pk=stationinmovie.part.movie.pk)
			
		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		station = Station.objects.get(pk=self.kwargs['station'])
		stationservices = StationService.objects.filter(station=station)
		transfers = station.get_group_station

		context['station'] = station
		context['stationservices'] = stationservices
		context['transfers'] = transfers

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']

		return context

class MovieListbyLineServiceView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/railway/movielistbylineservice.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		lineservice = LineService.objects.get(pk=self.kwargs['line_service'])
		lineinmovies = LineInMovie.objects.filter(line_service=lineservice)
		for lineinmovie in lineinmovies:
			if (lineinmovie.part):
				queryset |= Movie.objects.filter(pk=lineinmovie.part.movie.pk)

		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		lineservice = LineService.objects.get(pk=self.kwargs['line_service'])
		stationservices = StationService.objects.filter(line_service=lineservice)
		lines = lineservice.line.all()

		context['lineservice'] = lineservice
		context['stationservices'] = stationservices.exclude(is_representative=True).order_by('sort_by_line_service')
		context['lines'] = lines

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']

		context['admin'] = self.request.user.groups.filter(name='admin').exists()

		return context

class MovieListbyStationServiceView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/railway/movielistbystationservice.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		stationservice = StationService.objects.get(pk=self.kwargs['station_service'])
		stationinmovies = StationInMovie.objects.filter(station_service=stationservice)
		for stationinmovie in stationinmovies:
			if (stationinmovie.part):
				queryset |= Movie.objects.filter(pk=stationinmovie.part.movie.pk)

		stationservicegroup = stationservice.get_group_station_service()
		if stationservicegroup:
			if stationservicegroup.station.line == stationservice.station.line:
				stationinmovies = StationInMovie.objects.filter(station_service=stationservice)
				for stationinmovie in stationinmovies:
					if (stationinmovie.part):
						queryset |= Movie.objects.filter(pk=stationinmovie.part.movie.pk)

		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		stationservice = StationService.objects.get(pk=self.kwargs['station_service'])
		stations = stationservice.station.get_group_station()
		transfers = {}
		if stations:
			for station in stations:
				transfers[station] = StationService.objects.filter(station=station)

		different_line = False
		stationservicegroup = stationservice.get_group_station_service()
		if stationservicegroup:
			if stationservicegroup.station.line != stationservice.station.line:
				different_line = True

		context['stationservice'] = stationservice
		context['transfers'] = transfers
		context['stationservicegroup'] = stationservicegroup
		context['different_line'] = different_line

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']
		
		return context

class MusicTopView(generic.TemplateView):
	template_name = 'moviedatabase/music/songtop.html'

def r2k(kana):
	rk = {
		'a': ['ア', 'イ', 'ウ', 'エ', 'オ', ''],
		'k': ['カ', 'キ', 'ク', 'ケ', 'コ', ''],
		's': ['サ', 'シ', 'ス', 'セ', 'ソ', ''],
		't': ['タ', 'チ', 'ツ', 'テ', 'ト', ''],
		'n': ['ナ', 'ニ', 'ヌ', 'ネ', 'ノ', ''],
		'h': ['ハ', 'ヒ', 'フ', 'ヘ', 'ホ', ''],
		'm': ['マ', 'ミ', 'ム', 'メ', 'モ', ''],
		'y': ['ヤ', '', 'ユ', '', 'ヨ', ''],
		'r': ['ラ', 'リ', 'ル', 'レ', 'ロ', ''],
		'w': ['ワ', '', '', '', 'ヲ', 'ン']
	}
	row = {
		'a': 0,
		'i': 1,
		'u': 2,
		'e': 3,
		'o': 4,
		'n': 5
	}
	if len(kana) > 1:
		return rk[kana[0]][row[kana[1]]]
	else:
		return rk[kana[0]]

def get_dh(kana):
	dh = {
		'ウ': ['ヴ'],
		'カ': ['ガ'],
		'キ': ['ギ'],
		'ク': ['グ'],
		'ケ': ['ゲ'],
		'コ': ['ゴ'],
		'サ': ['ザ'],
		'シ': ['ジ'],
		'ス': ['ズ'],
		'セ': ['ゼ'],
		'ソ': ['ゾ'],
		'タ': ['ダ'],
		'チ': ['ヂ'],
		'ツ': ['ヅ'],
		'テ': ['デ'],
		'ト': ['ド'],
		'ハ': ['バ', 'パ'],
		'ヒ': ['ビ', 'ピ'],
		'フ': ['ブ', 'プ'],
		'ヘ': ['ベ', 'ペ'],
		'ホ': ['ボ', 'ポ'],
	}
	if kana in dh:
		return dh[kana[0]]
	else:
		return []

def initial_query(q, kana):
	kana = r2k(kana)
	if len(kana) == 1:
		q2 = q.none()
		q2 |= q.filter(name_kana__istartswith=kana)
		for d in get_dh(kana):
			q2 |= q.filter(name_kana__istartswith=d)
		return q2.order_by('name_kana')
	else:
		q2 = q.none()
		for k in kana:
			if k:
				q2 |= q.filter(name_kana__istartswith=k)
				for d in get_dh(k):
					q2 |= q.filter(name_kana__istartswith=d)
		return q2.order_by('name_kana')

class ArtistListView(generic.ListView):
	model = Artist
	paginate_by = 30
	template_name = 'moviedatabase/music/artistlist.html'

	def get_queryset(self):
		kana = self.kwargs['kana']
		queryset = Artist.objects.all().order_by('name_kana')
		if kana != "all":
			queryset = initial_query(queryset, kana)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		kana = self.kwargs['kana']
		if kana == "all":
			kana = "すべて"
		else:
			kana = r2k(kana)
			if len(kana) != 1:
				kana = kana[0] + "行"
		
		context['kana'] = kana

		return context

class SongListView(generic.ListView):
	model = Song
	paginate_by = 30
	template_name = 'moviedatabase/music/songlist.html'

	def get_queryset(self):
		kana = self.kwargs['kana']
		queryset = Song.objects.all().order_by('name_kana')
		if kana != "all":
			queryset = initial_query(queryset, kana)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		kana = self.kwargs['kana']
		if kana == "all":
			kana = "すべて"
		else:
			kana = r2k(kana)
			if len(kana) != 1:
				kana = kana[0] + "行"
		
		context['kana'] = kana

		return context

class SongListbyArtistView(generic.ListView):
	model = Song
	paginate_by = 30
	template_name = 'moviedatabase/music/songlistbyartist.html'

	def get_queryset(self):
		kana = self.kwargs['kana']
		queryset = Song.objects.filter(artist=self.kwargs['artist']).order_by('name_kana')
		if kana != "all":
			queryset = initial_query(queryset, kana)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		artist = Artist.objects.get(pk=self.kwargs['artist'])

		kana = self.kwargs['kana']
		if kana == "all":
			kana = "すべて"
		else:
			kana = r2k(kana)
			if len(kana) != 1:
				kana = kana[0] + "行"
		
		context['artist'] = artist
		context['kana'] = kana

		return context

class VocalListView(generic.ListView):
	model = VocalNew
	paginate_by = 30
	template_name = 'moviedatabase/music/vocallist.html'

class ArtistSearchView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/music/artistsearch.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		word = self.request.GET.get('word')
		if word:
			songnews = SongNew.objects.filter(Q(artist_name__icontains=word) | Q(artist_name_kana__icontains=word)).order_by('artist_name_kana')
			
			for song in songnews:
				queryset |= Movie.objects.filter(songnew=song)
				parts = Part.objects.filter(songnew=song)
				for part in parts:
					queryset |= Movie.objects.filter(pk=part.movie.pk)
		
		queryset = queryset.exclude(is_active=False).order_by('-published_at').distinct()
		sort = "pub"
		order = "n"
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		word = self.request.GET.get('word')
		context['word'] = word

		return context

class SongSearchView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/music/songsearch.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		word = self.request.GET.get('word')
		if word:
			songnews = SongNew.objects.filter(Q(song_name__icontains=word) | Q(song_name_kana__icontains=word) | Q(tag__icontains=word)).order_by('song_name_kana')
			
			for song in songnews:
				queryset |= Movie.objects.filter(songnew=song)
				parts = Part.objects.filter(songnew=song)
				for part in parts:
					queryset |= Movie.objects.filter(pk=part.movie.pk)
		
		queryset = queryset.exclude(is_active=False).order_by('-published_at').distinct()
		sort = "pub"
		order = "n"
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		word = self.request.GET.get('word')
		context['word'] = word

		return context

class MovieListbyArtistView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/music/movielistbyartist.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		artist = Artist.objects.get(pk=self.kwargs['artist'])
		songs = Song.objects.filter(artist=artist)
		for song in songs:
			queryset |= Movie.objects.filter(song=song)
			parts = Part.objects.filter(song=song)
			for part in parts:
				queryset |= Movie.objects.filter(pk=part.movie.pk)
			
		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		artist = Artist.objects.get(pk=self.kwargs['artist'])
		songs = Song.objects.filter(artist=artist)[:8]

		context['artist'] = artist
		context['songs'] = songs

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']

		return context

class MovieListbySongView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/music/movielistbysong.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		queryset |= Movie.objects.filter(song=self.kwargs['song'])
		parts = Part.objects.filter(song=self.kwargs['song'])
		for part in parts:
			queryset |= Movie.objects.filter(pk=part.movie.pk)
			
		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		song = Song.objects.get(pk=self.kwargs['song'])
		
		context['song'] = song
		context['artist'] = song.artist.all()

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']

		return context

class MovieListbyVocalView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/music/movielistbyvocal.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		queryset |= Movie.objects.filter(vocalnew=self.kwargs['vocal'])
		parts = Part.objects.filter(vocalnew=self.kwargs['vocal'])
		for part in parts:
			queryset |= Movie.objects.filter(pk=part.movie.pk)
			
		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		vocal = VocalNew.objects.get(pk=self.kwargs['vocal'])
		
		context['vocal'] = vocal

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']

		return context

class CreatorListView(generic.ListView):
	model = Creator
	paginate_by = 200
	template_name = 'moviedatabase/creator/creatorlist.html'

	def get_queryset(self):
		kana = self.kwargs['kana']
		queryset = Creator.objects.all().order_by('name_kana')
		if kana != "all":
			queryset = initial_query(queryset, kana)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		kana = self.kwargs['kana']
		if kana == "all":
			kana = "すべて"
		else:
			kana = r2k(kana)
			if len(kana) != 1:
				kana = kana[0] + "行"
		
		context['kana'] = kana

		return context

class ChannelListView(generic.ListView):
	model = YoutubeChannel
	paginate_by = 30
	template_name = 'moviedatabase/creator/youtubechannellist.html'

class CreatorSearchView(generic.ListView):
	model = Creator
	paginate_by = 30
	template_name = 'moviedatabase/creator/creatorsearch.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Creator.objects.none()
		word = self.request.GET.get('word')
		if word:
			queryset = Creator.objects.filter(Q(name__icontains=word) | Q(name_kana__icontains=word)).order_by('name_kana')
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		word = self.request.GET.get('word')
		context['word'] = word
		context['count'] = context['creator_list'].count()

		return context

class MovieListbyCreatorView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/creator/movielistbycreator.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		names = Name.objects.filter(creator=self.kwargs['creator'])
		for name in names:
			parts = Part.objects.filter(participant=name)
			for part in parts:
				queryset |= Movie.objects.filter(pk=part.movie.pk)
			
		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		creator = Creator.objects.get(pk=self.kwargs['creator'])
		names = Name.objects.filter(creator=creator)
		mainchannel = YoutubeChannel.objects.filter(creator=creator).filter(is_main=True)
		subchannel = YoutubeChannel.objects.filter(creator=creator).exclude(is_main=True)
		mainniconico = NiconicoAccount.objects.filter(creator=creator).filter(is_main=True)
		subniconico = NiconicoAccount.objects.filter(creator=creator).exclude(is_main=True)
		maintwitter = TwitterAccount.objects.filter(creator=creator).filter(is_main=True)
		subtwitter = TwitterAccount.objects.filter(creator=creator).exclude(is_main=True)
		pagelink = PageLink.objects.filter(creator=creator)

		context['creator'] = creator
		context['names'] = names
		context['mainchannel'] = mainchannel
		context['subchannel'] = subchannel
		context['mainniconico'] = mainniconico
		context['subniconico'] = subniconico
		context['maintwitter'] = maintwitter
		context['subtwitter'] = subtwitter
		context['pagelink'] = pagelink

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']

		admin = self.request.user.groups.filter(name='admin').exists()

		context['admin'] = admin

		return context

class MovieListbyNameView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/creator/movielistbyname.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		name = Name.objects.get(pk=self.kwargs['name'])
		parts = Part.objects.filter(participant=name)
		for part in parts:
			queryset |= Movie.objects.filter(pk=part.movie.pk)
			
		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		name = Name.objects.get(pk=self.kwargs['name'])

		context['name'] = name

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']

		return context

class MovieListbyChannelView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/creator/movielistbychannel.html'

	def get_queryset(self):
		queryset = Movie.objects.filter(channel=self.kwargs['channel_id']).exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		channel = YoutubeChannel.objects.get(pk=self.kwargs['channel_id'])
		
		context['channel'] = channel

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']

		return context

class MovieListbyNiconicoView(generic.ListView):
	model = Movie
	paginate_by = 15
	template_name = 'moviedatabase/creator/movielistbyniconico.html'

	def get_queryset(self):
		queryset = Movie.objects.filter(niconico_account=self.kwargs['niconico_account']).exclude(is_active=False).order_by('-published_at')
		sort = self.kwargs['sort']
		order = self.kwargs['order']
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		niconico = NiconicoAccount.objects.get(pk=self.kwargs['niconico_account'])
		
		context['niconico'] = niconico

		context['sort'] = self.kwargs['sort']
		context['order'] = self.kwargs['order']

		return context

def add_updatehistory(request, main_id, category):
	movie = Movie.objects.get(main_id=main_id)
	i = UpdateHistory(movie=movie, user=request.user, reg_date=timezone.now(), category=category)
	i.save()

@permission_required('moviedatabase.add_movie')
def confirm_movie(request, main_id):
	if not can_edit_channel(request, main_id):
		return redirect('moviedatabase:login')

	add_updatehistory(request, main_id, 'access-confirm')

	movie = get_object_or_404(Movie, main_id=main_id)
	parts = Part.objects.filter(movie=movie).order_by('sort_by_movie')
	if parts.count() == 1:
		onlyonepart = True
	else:
		onlyonepart = False

	can_edit = request.user.groups.filter(name='can_edit').exists()

	context = {
		'movie': movie,
		'parts': parts,
		'onlyonepart': onlyonepart,
		'can_edit': can_edit,
		'type': "confirm"
	}

	return render(request, 'moviedatabase/detail.html', context)

def detail_movie(request, main_id):
	movie = get_object_or_404(Movie, main_id=main_id)
	parts = Part.objects.filter(movie=movie).order_by('sort_by_movie')
	if parts.count() == 1:
		onlyonepart = True
	else:
		onlyonepart = False

	can_edit = request.user.groups.filter(name='can_edit').exists()
	can_edit = can_edit and can_edit_channel(request, main_id)

	if 'confirm' in request.POST:
		add_updatehistory(request, main_id, 'complete-confirm')
		info = MovieUpdateInformation.objects.filter(movie=movie)
		if info:
			t = 'U'
		else:
			t = 'C'
		i = MovieUpdateInformation(movie=movie, creator=None, is_create=t, user=request.user, reg_date=timezone.now())
		i.save()
		movie.update_date = timezone.now()
		movie.save()

	context = {
		'movie': movie,
		'parts': parts,
		'onlyonepart': onlyonepart,
		'can_edit': can_edit,
		'type': "detail"
	}

	return render(request, 'moviedatabase/detail.html', context)

class MovieRegisterView(PermissionRequiredMixin, generic.CreateView):
	template_name = 'moviedatabase/register.html'
	model = Movie
	form_class = forms.MovieRegisterForm
	permission_required = ('moviedatabase.add_movie')

	def get_form_kwargs(self):
		kw = super(MovieRegisterView, self).get_form_kwargs()
		kw['request'] = self.request
		return kw
		
	def get_success_url(self):
		return reverse_lazy('moviedatabase:movie_edit', kwargs={'main_id': self.object.main_id})

def can_edit_channel(request, main_id):
	cs = request.user.all_can_edit_channel()
	movie = Movie.objects.get(main_id=main_id)
	flag = False

	for c in cs:
		if (c == movie.channel):
			flag = True
	return flag

@permission_required('moviedatabase.add_movie')
def movie_edit(request, main_id):
	if not can_edit_channel(request, main_id):
		return redirect('moviedatabase:login')

	add_updatehistory(request, main_id, 'access-movie-edit')

	movie = get_object_or_404(Movie, main_id=main_id)
	form = forms.MovieUpdateForm(request.POST or None, instance=movie)
	parts = Part.objects.filter(movie=main_id)
	partcount = parts.count()
	if request.method == 'POST' and form.is_valid():
		form.save()
		if partcount == 0 and ('single' in request.POST):
			p = Part.objects.create(sort_by_movie="0", short_name="0", name="", movie=movie, start_time=datetime.timedelta(0))
			p.participant.add(movie.channel.main_name)
			songs = movie.songnew.all()
			for song in songs:
				p.songnew.add(song)
			return redirect('moviedatabase:station_edit', main_id=main_id, sort_by_movie=0)
		elif partcount == 1:
			f = parts.first()
			return redirect('moviedatabase:station_edit', main_id=main_id, sort_by_movie=f.sort_by_movie)
		return redirect('moviedatabase:part_edit', main_id=main_id)

	context = {
		'movie': movie,
		'form': form,
		'parts': parts,
		'partcount': partcount
	}

	return render(request, 'moviedatabase/movie_edit.html', context)

@permission_required('moviedatabase.add_part')
def movie_part_edit(request, main_id):
	if not can_edit_channel(request, main_id):
		return redirect('moviedatabase:login')

	add_updatehistory(request, main_id, 'access-part-edit')

	movie = get_object_or_404(Movie, main_id=main_id)
	form = forms.MovieUpdateForm(request.POST or None, instance=movie)
	formset = forms.PartEditFormset(request.POST or None, instance=movie)
	if request.method == 'POST' and form.is_valid() and formset.is_valid():
		form.save()
		formset.save()
		firstpart = Part.objects.filter(movie=main_id).order_by('sort_by_movie').first()
		if firstpart:
			return redirect('moviedatabase:station_edit', main_id=main_id, sort_by_movie=firstpart.sort_by_movie)
		else:
			return redirect('moviedatabase:detail', main_id=main_id)

	context = {
		'movie': movie,
		'form': form,
		'formset': formset
	}

	return render(request, 'moviedatabase/part_edit.html', context)

@permission_required('moviedatabase.add_stationinmovie')
def movie_part_station_edit(request, main_id, sort_by_movie):
	if not can_edit_channel(request, main_id):
		return redirect('moviedatabase:login')

	add_updatehistory(request, main_id, 'access-part-station-edit')

	part = get_object_or_404(Part, movie=main_id, sort_by_movie=sort_by_movie)
	part_form = forms.PartEditForm(request.POST or None, instance=part)
	formset = forms.StationInMovieEditFormset(request.POST or None, instance=part)
	if request.method == 'POST' and part_form.is_valid() and formset.is_valid():
		part_form.save()
		formset.save()

		stations = StationInMovie.objects.filter(part=part)

		lines = LineInMovie.objects.filter(part=part)
		lines.delete()
		lines = LineService.objects.none()
		lineinmovies = []
		for station in stations:
			lines |= LineService.objects.filter(pk=station.station_service.line_service.pk)
		for line in lines:
			lineinmovie = LineInMovie(part=part, line_service=line)
			lineinmovies.append(lineinmovie)
		LineInMovie.objects.bulk_create(lineinmovies)

		queryset = Part.objects.filter(movie=main_id, sort_by_movie=sort_by_movie+1)
		if queryset.first() is None:
			return redirect('moviedatabase:confirm', main_id=main_id)
		else:
			return redirect('moviedatabase:station_edit', main_id=main_id, sort_by_movie=sort_by_movie+1)

	partcount = Part.objects.filter(movie=main_id).count()
	prefs = Prefecture.objects.all()
	companies = Company.objects.all()

	context = {
		'part': part,
		'part_form': part_form,
		'formset': formset,
		'prefs': prefs,
		'companies': companies,
		'partcount': partcount
	}

	return render(request, 'moviedatabase/station_edit.html', context)

class NameCreate(PermissionRequiredMixin, generic.CreateView):
	model = Name
	fields = '__all__'
	permission_required = ('moviedatabase.add_name')
	success_url = reverse_lazy('moviedatabase:top')

class PopupNameCreate(NameCreate):
	def form_valid(self, form):
		name = form.save()
		context = {
			'object_name': str(name),
			'object_pk': name.pk,
			'function_name': 'add_name'
		}
		return render(self.request, 'moviedatabase/close_name.html', context)


@permission_required('moviedatabase.add_movie')
def popup_parent_movie_setting(request):
	if request.method == 'POST':
		context = {
			'movie_list': request.POST['selected-movie-list'],
			'movie_type': "parent"
		}
		return render(request, 'moviedatabase/close_movie_setting.html', context)

	channels = YoutubeChannel.objects.all()
	movies = Movie.objects.all()

	context = {
		'channels': channels,
		'movies': movies,
		'movie_type': "parent"
	}

	return render(request, 'moviedatabase/movie_setting.html', context)

@permission_required('moviedatabase.add_movie')
def popup_related_movie_setting(request):
	if request.method == 'POST':

		context = {
			'movie_list': request.POST['selected-movie-list'],
			'movie_type': "related"
		}
		return render(request, 'moviedatabase/close_movie_setting.html', context)

	channels = YoutubeChannel.objects.all()
	movies = Movie.objects.all()

	context = {
		'channels': channels,
		'movies': movies,
		'movie_type': "related"
	}

	return render(request, 'moviedatabase/movie_setting.html', context)

@permission_required('moviedatabase.add_movie')
def popup_participant_setting(request):
	if request.method == 'POST':

		context = {
			'participant_list': request.POST['selected-participant-list'],
		}
		return render(request, 'moviedatabase/close_participant_setting.html', context)

	creators = Creator.objects.all()
	names = Name.objects.all()

	context = {
		'creators': creators,
		'names': names,
	}

	return render(request, 'moviedatabase/participant_setting.html', context)

@permission_required('moviedatabase.add_movieupdateinformation')
def UpdateInformation(request, main_id):
	movie = get_object_or_404(Movie, main_id=main_id)
	info = MovieUpdateInformation.objects.filter(movie=movie)
	if info:
		t = 'U'
	else:
		t = 'C'
	i = MovieUpdateInformation(movie=movie, creator=None, is_create=t, reg_date=timezone.now())
	i.save()
	movie.update_date = timezone.now()
	movie.save()

	return redirect('moviedatabase:detail', main_id=main_id)

@permission_required('moviedatabase.add_movieupdateinformation')
def UpdateInformationforCreator(request, creator):
	creator = get_object_or_404(Creator, id=creator)
	info = MovieUpdateInformation.objects.filter(creator=creator)
	if info:
		t = 'U'
	else:
		t = 'C'
		i = MovieUpdateInformation(movie=None, creator=creator, is_create='C', reg_date=timezone.now())
		i.save()

	return redirect('moviedatabase:movielistbycreator', creator=creator.pk, sort='pub', order='n')

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

class StationServiceSearchViewSet(generics.ListAPIView):
	serializer_class = serializer.StationServiceSerializer
	def get_queryset(self):
		q = self.kwargs['word']
		return StationService.objects.filter(name__contains=q)

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