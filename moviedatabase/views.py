from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone
from rest_framework import generics
from . import serializer
from django.db.models import Q
from pure_pagination.mixins import PaginationMixin

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

import pytz
from dateutil import relativedelta
import datetime

from io import TextIOWrapper
import csv

import re

# Create your views here.

def test(request):
	stations = StationInMovie.objects.all()
	for station in stations:
		if (station.line_name_customize is None or station.line_name_customize == ""):
			station.line_name_customize = station.station_service.line_service.__str__()
			station.save()
	parts = Part.objects.all()
	for part in parts:
		if (part.information_time_point is None):
			original_date = datetime.date(part.movie.published_at_year, part.movie.published_at_month, part.movie.published_at_day)
			part.information_time_point = original_date
			part.save()

def todaymovie():
	JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
	now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
	m = Movie.objects.filter(published_at_month=now.month, published_at_day=now.day)
	
	return m

class Top(generic.ListView):
	model = Movie
	template_name = 'moviedatabase/top.html'


	def get_context_data(self):
		movies = Movie.objects.all().exclude(is_active=False)[:6]
		update_list = MovieUpdateInformation.objects.all()[:10]
		notice_list = NoticeInformation.objects.all()[:10]
		top_img = TopImage.objects.all().order_by("?").first()
		context = {
			'top_img': top_img,
			'movie_list': movies,
			'todaymovie': todaymovie().order_by("?").first(),
			'today': timezone.now(),
			'update_list': update_list,
			'notice_list': notice_list
		}

		return context

class NoticeList(PaginationMixin, generic.ListView):
	model = NoticeInformation
	paginate_by = 30
	template_name = 'moviedatabase/notice/notice_list.html'

class UpdateList(PaginationMixin, generic.ListView):
	model = MovieUpdateInformation
	paginate_by = 30
	template_name = 'moviedatabase/notice/update_list.html'

class NoticeDetail(generic.DetailView):
	model = NoticeInformation
	template_name = 'moviedatabase/notice/notice_detail.html'

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

def Privacy(request):
	return render(request, 'moviedatabase/static-page/privacy.html')

def Update(request):
	return render(request, 'moviedatabase/static-page/update.html')

def GuideAccountCreator(request):
	return render(request, 'moviedatabase/static-page/guide-account-creator.html')

def StartUpGuide(request):
	return render(request, 'moviedatabase/static-page/startup-guide.html')

def LineCustomizeGuide(request):
	return render(request, 'moviedatabase/static-page/line-customize-guide.html')

class MovieListView(PaginationMixin, generic.ListView):
	model = Movie
	template_name = 'moviedatabase/movielist.html'
	queryset = Movie.objects.all()
	paginate_by = 30
	ordering = '-published_at'

	def get_queryset(self):
		queryset = super().get_queryset()

		word = self.request.GET.get('word')
		if word:
			queryset = queryset.filter(Q(title__icontains=word) | Q(main_id__icontains=word) | Q(description__icontains=word) | Q(explanation__icontains=word))
			parts = Part.objects.filter(Q(name__icontains=word) | Q(explanation__icontains=word))
			queryset_by_part = Movie.objects.none()
			for part in parts:
				queryset_by_part |= Movie.objects.filter(pk=part.movie.pk)
			queryset |= queryset_by_part

		q_is_collab = self.request.GET.getlist('is_collab')
		if q_is_collab:
			movies_is_collab = Movie.objects.none()
			for q in q_is_collab:
				movies_is_collab |= queryset.filter(is_collab=q)
			queryset = movies_is_collab

		q_channel = self.request.GET.get('channel')
		if q_channel:
			queryset = queryset.filter(channel__name__icontains=q_channel)

		q_sung_name = self.request.GET.get('sung_name')
		if q_sung_name:
			movies_sungname = Movie.objects.none()
			stationinmovies = StationInMovie.objects.filter(sung_name__icontains=q_sung_name)
			for s in stationinmovies:
				if (s.part):
					movies_sungname |= Movie.objects.filter(pk=s.part.movie.pk)
			queryset &= movies_sungname

		q_line_name_customize = self.request.GET.get('line_name_customize')
		if q_line_name_customize:
			movies_linenamecustomize = Movie.objects.none()
			stationinmovies = StationInMovie.objects.filter(line_name_customize__icontains=q_line_name_customize)
			for s in stationinmovies:
				if (s.part):
					movies_linenamecustomize |= Movie.objects.filter(pk=s.part.movie.pk)
			queryset &= movies_linenamecustomize

		q_artist = self.request.GET.get('artist')
		if q_artist:
			movies_artist = Movie.objects.none()
			songnews = SongNew.objects.filter(Q(artist_name__icontains=q_artist) | Q(artist_name_kana__icontains=q_artist)).order_by('artist_name_kana')
			for song in songnews:
				movies_artist |= Movie.objects.filter(songnew=song)
				parts = Part.objects.filter(songnew=song)
				for part in parts:
					movies_artist |= Movie.objects.filter(pk=part.movie.pk)
			queryset &= movies_artist

		q_song = self.request.GET.get('song')
		if q_song:
			movies_song = Movie.objects.none()
			songnews = SongNew.objects.filter(Q(song_name__icontains=q_song) | Q(song_name_kana__icontains=q_song)).order_by('song_name_kana')
			for song in songnews:
				movies_song |= Movie.objects.filter(songnew=song)
				parts = Part.objects.filter(songnew=song)
				for part in parts:
					movies_song |= Movie.objects.filter(pk=part.movie.pk)
			queryset &= movies_song


		JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
		q_published_at_start = self.request.GET.get('published_at_start')
		q_published_at_end = self.request.GET.get('published_at_end')

		if q_published_at_start and q_published_at_end:
			q_published_at_start = datetime.datetime.strptime(q_published_at_start, '%Y-%m-%dT%H:%M').astimezone(JST)
			q_published_at_end = datetime.datetime.strptime(q_published_at_end, '%Y-%m-%dT%H:%M').astimezone(JST)
			queryset = queryset.filter(published_at__gte=q_published_at_start, published_at__lte=q_published_at_end)
		
		q_information_time_point_start = self.request.GET.get('information_time_point_start')
		q_information_time_point_end = self.request.GET.get('information_time_point_end')

		if q_information_time_point_start and q_information_time_point_end:
			movies_infotime = Movie.objects.none()
			parts = Part.objects.filter(information_time_point__gte=q_information_time_point_start, information_time_point__lte=q_information_time_point_end)
			for part in parts:
				movies_infotime |= Movie.objects.filter(pk=part.movie.pk)
			queryset &= movies_infotime
		
		queryset = queryset.exclude(is_active=False).order_by('-published_at').distinct()
		return moviequery(queryset, "pub", "n")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		context['word'] = self.request.GET.get('word')
		context['is_collab'] = self.request.GET.getlist('is_collab')
		context['channel'] = self.request.GET.get('channel')
		context['sung_name'] = self.request.GET.get('sung_name')
		context['line_name_customize'] = self.request.GET.get('line_name_customize')
		context['song'] = self.request.GET.get('song')
		context['artist'] = self.request.GET.get('artist')
		context['published_at_start'] = self.request.GET.get('published_at_start')
		context['published_at_end'] = self.request.GET.get('published_at_end')
		context['information_time_point_start'] = self.request.GET.get('information_time_point_start')
		context['information_time_point_end'] = self.request.GET.get('information_time_point_end')
		context['is_detail_search'] = False

		if (context['word'] or context['is_collab'] or context['channel'] or context['sung_name'] or context['line_name_customize'] or context['song'] or context['artist'] or context['published_at_start'] or context['published_at_end'] or context['information_time_point_start'] or context['information_time_point_end']):
			context['is_detail_search'] = True
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
	movies = movies.exclude(is_active=False).order_by('-published_at')[:5]

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

	movies_sungname = Movie.objects.none()
	if word:
		stationinmovies = StationInMovie.objects.filter(sung_name__icontains=word)
		for s in stationinmovies:
			if (s.part):
				movies_sungname |= Movie.objects.filter(pk=s.part.movie.pk)

	movies_sungname = movies_sungname.exclude(is_active=False).order_by('-published_at').distinct()
	sncount = movies_sungname.count
	movies_sungname = moviequery(movies_sungname, "pub", "n")[:5]

	movies_songtag = Movie.objects.none()
	if word:
		songnews = SongNew.objects.filter(Q(tag__icontains=word)).order_by('song_name_kana')
		
		for song in songnews:
			movies_songtag |= Movie.objects.filter(songnew=song)
			parts = Part.objects.filter(songnew=song)
			for part in parts:
				movies_songtag |= Movie.objects.filter(pk=part.movie.pk)

	movies_songtag = movies_songtag.exclude(is_active=False).order_by('-published_at').distinct()
	tcount = movies_songtag.count
	movies_songtag = moviequery(movies_songtag, "pub", "n")[:5]

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
		songnews = SongNew.objects.filter(Q(song_name__icontains=word) | Q(song_name_kana__icontains=word)).order_by('song_name_kana')
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
		"movies_sungname": movies_sungname,
		"movies_songtag": movies_songtag,
		"movies_artist": movies_artist,
		"movies_song": movies_song,
		'mcount': mcount,
		'lcount': lcount,
		'scount': scount,
		'ccount': ccount,
		'sncount': sncount,
		'tcount': tcount,
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
		context['belongscategories'] = BelongsCategory.objects.exclude(name="鉄道")
		context['moviecategories'] = MovieCategory.objects.all()

		return context

class MovieListbyBelongsCategoryView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/railway/movielistbybelongscategory.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		category = BelongsCategory.objects.get(pk=self.kwargs['category'])
		stationservices = StationService.objects.filter(line_service__category=category)
		for s in stationservices:
			stationinmovies = StationInMovie.objects.filter(station_service=s)
			for sim in stationinmovies:
				if (sim.part.movie):
					queryset |= Movie.objects.filter(pk=sim.part.movie.pk)

		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = BelongsCategory.objects.exclude(name="鉄道")
		context['category'] = BelongsCategory.objects.get(pk=self.kwargs['category'])

		return context

class MovieListbyMovieCategoryView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/railway/movielistbymoviecategory.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		category = MovieCategory.objects.get(pk=self.kwargs['category'])
		parts = Part.objects.filter(category=category)
		for p in parts:
			if (p.movie):
				queryset |= Movie.objects.filter(pk=p.movie.pk)

		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = MovieCategory.objects.all()
		context['category'] = MovieCategory.objects.get(pk=self.kwargs['category'])

		return context

class CompanyListbyRegionView(PaginationMixin, generic.ListView):
	model = Company
	paginate_by = 30
	template_name = 'moviedatabase/railway/companylistbyregion.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Company.objects.none()
		region = Region.objects.get(pk=self.kwargs['region'])
		prefs = Prefecture.objects.filter(region=region)
	
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
		return context

class LineServiceListbyPrefectureView(PaginationMixin, generic.ListView):
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

class LineServiceListbyCompanyView(PaginationMixin, generic.ListView):
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

class LineServiceListbyCompanyandPrefectureView(PaginationMixin, generic.ListView):
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

class LineServiceSearchView(PaginationMixin, generic.ListView):
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

		return context

class StationServiceSearchView(PaginationMixin, generic.ListView):
	model = StationService
	paginate_by = 30
	template_name = 'moviedatabase/railway/stationservicesearch.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = StationService.objects.none()
		word = self.request.GET.get('word')
		
		if word:
			queryset = StationService.objects.filter(name__icontains=word)
			if self.request.GET.get('is_kana') == "true":
				queryset |= StationService.objects.filter(station__name_kana__icontains=word)
		return queryset.order_by('line_service')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		context['word'] = self.request.GET.get('word')
		context['is_kana'] = self.request.GET.get('is_kana')

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

class MovieListbyStationInMovieSearchView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/railway/movielistbystationinmoviesearch.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		word = self.request.GET.get('word')
		if word:
			stationinmovies = StationInMovie.objects.filter(sung_name__icontains=word)
			for s in stationinmovies:
				if (s.part):
					queryset |= Movie.objects.filter(pk=s.part.movie.pk)

		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		word = self.request.GET.get('word')
		context['word'] = word

		return context

class MovieListbyLineView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
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
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
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

		context['sort'] = self.request.GET.get('sort')
		context['order'] = self.request.GET.get('order')

		context['admin'] = self.request.user.groups.filter(name='admin').exists()

		return context

class MovieListbyStationView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
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
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		station = Station.objects.get(pk=self.kwargs['station'])
		stationservices = StationService.objects.filter(station=station)
		transfers = station.get_group_station

		context['station'] = station
		context['stationservices'] = stationservices
		context['transfers'] = transfers

		context['sort'] = self.request.GET.get('sort')
		context['order'] = self.request.GET.get('order')

		return context

class MovieListbyLineServiceView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
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
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		lineservice = LineService.objects.get(pk=self.kwargs['line_service'])
		stationservices = StationService.objects.filter(line_service=lineservice)
		lines = lineservice.line.all()

		context['lineservice'] = lineservice
		context['stationservices'] = stationservices.exclude(is_representative=True).order_by('sort_by_line_service')
		context['lines'] = lines

		context['sort'] = self.request.GET.get('sort')
		context['order'] = self.request.GET.get('order')

		context['admin'] = self.request.user.groups.filter(name='admin').exists()

		return context

class MovieListbyStationServiceView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
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
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
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

		context['sort'] = self.request.GET.get('sort')
		context['order'] = self.request.GET.get('order')
		
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

class ArtistSearchView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
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

class SongSearchView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/music/songsearch.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		word = self.request.GET.get('word')
		if word:
			songnews = SongNew.objects.filter(Q(song_name__icontains=word) | Q(song_name_kana__icontains=word)).order_by('song_name_kana')
			
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

class SongTagSearchView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/music/songtagsearch.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		word = self.request.GET.get('word')
		if word:
			songnews = SongNew.objects.filter(Q(tag__icontains=word)).order_by('song_name_kana')
			
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

class MovieListbyVocalView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/music/movielistbyvocal.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		parts = Part.objects.filter(vocalnew=self.kwargs['vocal'])
		for part in parts:
			queryset |= Movie.objects.filter(pk=part.movie.pk)
			
		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = "pub"
		order = "n"
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		vocal = VocalNew.objects.get(pk=self.kwargs['vocal'])
		
		context['vocal'] = vocal

		return context

class CreatorTopView(PaginationMixin, generic.ListView):
	model = Creator
	paginate_by = 200
	template_name = 'moviedatabase/creator/creatorlist.html'

	def get_queryset(self):
		kana = self.request.GET.get('kana')
		queryset = Creator.objects.all().order_by('name_kana')
		if kana:
			queryset = initial_query(queryset, kana)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		kana = self.request.GET.get('kana')
		if not kana:
			kana = "すべて"
		else:
			kana = r2k(kana)
			if len(kana) != 1:
				kana = kana[0] + "行"
		
		context['kana'] = kana

		return context

class ChannelListView(PaginationMixin, generic.ListView):
	model = YoutubeChannel
	paginate_by = 30
	template_name = 'moviedatabase/creator/youtubechannellist.html'

class CreatorSearchView(PaginationMixin, generic.ListView):
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

class MovieListbyCreatorView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
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
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
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

		context['sort'] = self.request.GET.get('sort')
		context['order'] = self.request.GET.get('order')

		admin = self.request.user.groups.filter(name='admin').exists()

		context['admin'] = admin

		return context

class MovieListbyNameView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/creator/movielistbyname.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = Movie.objects.none()
		name = Name.objects.get(pk=self.kwargs['name'])
		parts = Part.objects.filter(participant=name)
		for part in parts:
			queryset |= Movie.objects.filter(pk=part.movie.pk)
			
		queryset = queryset.exclude(is_active=False).order_by('-published_at')
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		name = Name.objects.get(pk=self.kwargs['name'])

		context['name'] = name

		context['sort'] = self.request.GET.get('sort')
		context['order'] = self.request.GET.get('order')

		return context

class MovieListbyChannelView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/creator/movielistbychannel.html'

	def get_queryset(self):
		queryset = Movie.objects.filter(channel=self.kwargs['channel_id']).exclude(is_active=False).order_by('-published_at')
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		channel = YoutubeChannel.objects.get(pk=self.kwargs['channel_id'])
		
		context['channel'] = channel

		context['sort'] = self.request.GET.get('sort')
		context['order'] = self.request.GET.get('order')

		context['admin'] = self.request.user.groups.filter(name='admin').exists()

		return context

class MovieListbyNiconicoView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/creator/movielistbyniconico.html'

	def get_queryset(self):
		queryset = Movie.objects.filter(niconico_account=self.kwargs['niconico_account']).exclude(is_active=False).order_by('-published_at')
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
		return moviequery(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		niconico = NiconicoAccount.objects.get(pk=self.kwargs['niconico_account'])
		
		context['niconico'] = niconico

		context['sort'] = self.request.GET.get('sort')
		context['order'] = self.request.GET.get('order')

		return context

def add_updatehistory(request, main_id, category):
	movie = Movie.objects.get(main_id=main_id)
	i = UpdateHistory(movie=movie, user=request.user, reg_date=timezone.now(), category=category)
	i.save()

def is_can_statistics_update(movie):
	JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
	now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
	day = datetime.datetime(now.year, now.month, now.day, 0, 0, tzinfo=JST)
	return day > movie.statistics_update_date
	# trueなら更新可能

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

	if (movie.is_active == False and can_edit == False):
		return render(request, '403.html')

	if 'confirm' in request.POST:
		for part in parts:
			lineinmovies = LineInMovie.objects.filter(part=part)
			categories = BelongsCategory.objects.none()
			for l in lineinmovies:
				categories |= BelongsCategory.objects.filter(pk=l.line_service.category.pk)
			text = ""

			for c in categories:
				if c.object_name and part.category:
					if part.category.object_name:
						text += (c.object_name + part.category.object_name) + '\n'
			part.complex_category = text
			part.save()

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
		'can_statistics_update': is_can_statistics_update(movie),
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

@permission_required('moviedatabase.add_movie')
def movie_statistics_update(request, main_id):
	movie = get_object_or_404(Movie, main_id=main_id)

	can_statistics_update = is_can_statistics_update(movie)
	if not can_statistics_update:
		return render(request, '403.html')	

	form = forms.MovieStatisticsUpdateForm(request.POST or None, instance=movie)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('moviedatabase:detail', main_id=main_id)

	context = {
		'movie': movie,
		'form': form
	}

	return render(request, 'moviedatabase/movie_statistics_update.html', context)


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

	original_date = datetime.date(part.movie.published_at_year, part.movie.published_at_month, part.movie.published_at_day)
	d = original_date if (part.information_time_point is None) else part.information_time_point

	initial_dict = {
		'information_time_point': d,
	}
	
	part_form = forms.PartEditForm(request.POST or None, instance=part, initial=initial_dict)
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
			if (station.line_name_customize is None or station.line_name_customize == ""):
				station.line_name_customize = station.station_service.line_service.__str__()
				station.save()
			lines |= LineService.objects.filter(pk=station.station_service.line_service.pk)
		for line in lines:
			lineinmovie = LineInMovie(part=part, line_service=line)
			lineinmovies.append(lineinmovie)
		LineInMovie.objects.filter(part=part).delete()
		LineInMovie.objects.bulk_create(lineinmovies)

		queryset = Part.objects.filter(movie=main_id, sort_by_movie=sort_by_movie+1)
		if queryset.first() is None:
			return redirect('moviedatabase:confirm', main_id=main_id)
		else:
			return redirect('moviedatabase:station_edit', main_id=main_id, sort_by_movie=sort_by_movie+1)

	partcount = Part.objects.filter(movie=main_id).count()
	prefs = Prefecture.objects.all()
	companies = Company.objects.all()
	other_stations = StationService.objects.filter(line_service__company__other_option=True).filter(is_representative=False)
	other_lines = StationService.objects.filter(line_service__company__other_option=True).filter(is_representative=True)

	context = {
		'part': part,
		'part_form': part_form,
		'formset': formset,
		'original_date': original_date,
		'prefs': prefs,
		'companies': companies,
		'other_stations': other_stations,
		'other_lines': other_lines,
		'partcount': partcount
	}

	return render(request, 'moviedatabase/station_edit.html', context)

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

class NameCreate(PermissionRequiredMixin, generic.CreateView):
	model = Name
	fields = '__all__'
	permission_required = ('moviedatabase.add_name')
	template_name = "moviedatabase/edit_setting/name_form.html"
	success_url = reverse_lazy('moviedatabase:top')

class PopupNameCreate(NameCreate):
	def form_valid(self, form):
		name = form.save()
		context = {
			'object_name': str(name),
			'object_pk': name.pk,
			'function_name': 'add_name'
		}
		return render(self.request, 'moviedatabase/edit_setting/close_name.html', context)


@permission_required('moviedatabase.add_movie')
def popup_parent_movie_setting(request):
	if request.method == 'POST':
		context = {
			'movie_list': request.POST['selected-movie-list'],
			'movie_type': "parent"
		}
		return render(request, 'moviedatabase/edit_setting/close_movie_setting.html', context)

	channels = YoutubeChannel.objects.all()
	movies = Movie.objects.all()

	context = {
		'channels': channels,
		'movies': movies,
		'movie_type': "parent"
	}

	return render(request, 'moviedatabase/edit_setting/movie_setting.html', context)

@permission_required('moviedatabase.add_movie')
def popup_related_movie_setting(request):
	if request.method == 'POST':

		context = {
			'movie_list': request.POST['selected-movie-list'],
			'movie_type': "related"
		}
		return render(request, 'moviedatabase/edit_setting/close_movie_setting.html', context)

	channels = YoutubeChannel.objects.all()
	movies = Movie.objects.all()

	context = {
		'channels': channels,
		'movies': movies,
		'movie_type': "related"
	}

	return render(request, 'moviedatabase/edit_setting/movie_setting.html', context)

@permission_required('moviedatabase.add_movie')
def popup_participant_setting(request):
	if request.method == 'POST':

		context = {
			'participant_list': request.POST['selected-participant-list'],
		}
		return render(request, 'moviedatabase/edit_setting/close_participant_setting.html', context)

	creators = Creator.objects.all()
	names = Name.objects.all()

	context = {
		'creators': creators,
		'names': names,
	}

	return render(request, 'moviedatabase/edit_setting/participant_setting.html', context)

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

def AccountAndCreatorApplicationView(request):
	if (request.user is None):
		return render(request, '403.html')

	context = {
		'user': request.user,
		'creators': Creator.objects.all()
	}

	return render(request, 'moviedatabase/application/account_and_creator.html', context)

def AccountAndCreatorApplicationConfirmView(request, creator):
	if (request.user is None or request.user.creator_applied):
		return render(request, '403.html')
	creator = Creator.objects.get(pk=creator)

	context = {
		'user': request.user,
		'creator': creator
	}

	if request.method == 'POST':
		request.user.creator_applied = True
		request.user.save()
		dealing = request.POST['dealing']
		ac = AccountAndCreatorApplication(user=request.user, creator=creator, reg_date=timezone.now(), dealing=dealing)
		ac.save()
		return render(request, 'moviedatabase/application/account_and_creator_complete.html', context)

	return render(request, 'moviedatabase/application/account_and_creator_confirm.html', context)

@permission_required('moviedatabase.add_youtubechannel')
def ChannelMovieIsExist(request, channel_id):
	channel = get_object_or_404(YoutubeChannel, channel_id=channel_id)
	context = {
		'channel': channel,
		'movies': Movie.objects.filter(channel=channel)
	}
	return render(request, 'moviedatabase/channel_movie_is_exist.html', context)

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