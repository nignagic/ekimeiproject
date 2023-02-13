from django.views import generic
from ..models import *

from django.shortcuts import get_object_or_404
from pure_pagination.mixins import PaginationMixin
from django.db.models import Q

from .searchsets import *

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

		category = BelongsCategory.objects.get(pk=self.kwargs['category'])
		queryset = queryset.filter(
			part__stationinmovie__station_service__line_service__category=category
		)

		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
		
		return organize_movie_query(queryset, sort, order)

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

		category = MovieCategory.objects.get(pk=self.kwargs['category'])
		queryset = queryset.filter(
			part__category=category
		)

		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')

		return organize_movie_query(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = MovieCategory.objects.all()
		context['category'] = MovieCategory.objects.get(pk=self.kwargs['category'])

		return context

class LineServiceListbyPrefectureView(PaginationMixin, generic.ListView):
	model = LineService
	paginate_by = 50
	template_name = 'moviedatabase/railway/lineservicelistbyprefecture.html'

	def get_queryset(self):
		queryset = super().get_queryset()

		pref = Prefecture.objects.get(pk=self.kwargs['pref'])
		queryset = queryset.filter(prefs=pref).order_by('company', 'sort_by_company')
		
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		pref = Prefecture.objects.get(pk=self.kwargs['pref'])
		companies = Company.objects.filter(
			lineservice__prefs=pref
		).distinct()

		context['pref'] = pref
		context['companies'] = companies

		return context

class LineServiceListbyCompanyView(PaginationMixin, generic.ListView):
	model = LineService
	paginate_by = 30
	template_name = 'moviedatabase/railway/lineservicelistbycompany.html'

	def get_queryset(self):
		queryset = super().get_queryset()

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

class MovieListbyStationInMovieSearchView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/railway/movielistbystationinmoviesearch.html'

	def get_queryset(self):
		queryset = super().get_queryset()

		word = self.request.GET.get('word')
		if word:
			queryset = search_sung_name(queryset, word)

		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')

		return organize_movie_query(queryset, sort, order)

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

		line = Line.objects.get(pk=self.kwargs['line'])
		queryset = queryset.filter(
			part__stationinmovie__station_service__station__line__pk=line.pk
		)
			
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')

		return organize_movie_query(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		line = Line.objects.get(pk=self.kwargs['line'])
		stations = Station.objects.filter(line=line).order_by('sort_by_line')
		lineservices = LineService.objects.filter(
			stationservice__station__line=line
		).distinct()
		
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

		station = get_object_or_404(Station, pk=self.kwargs['station'])
		queryset = queryset.filter(
			part__stationinmovie__station_service__station__pk=station.pk
		)

		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')

		return organize_movie_query(queryset, sort, order)

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

# このテンプレートの高速化をしたい
class MovieListbyLineServiceView(PaginationMixin, generic.ListView):
	model = Movie
	paginate_by = 30
	template_name = 'moviedatabase/railway/movielistbylineservice.html'

	def get_queryset(self):
		queryset = super().get_queryset()

		lineservice = get_object_or_404(LineService, pk=self.kwargs['line_service'])
		queryset = Movie.objects.filter(
			part__stationinmovie__station_service__line_service__pk=lineservice.pk
		)

		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')

		return organize_movie_query(queryset, sort, order)

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

		stationservice = get_object_or_404(StationService, pk=self.kwargs['station_service'])
		queryset = Movie.objects.filter(
			part__stationinmovie__station_service__pk=stationservice.pk
		)
			
		# 駅グループが存在する場合
		# （山手線の東京駅、山陽本線の岡山駅など）
		stationservicegroup = stationservice.get_group_station_service()
		if stationservicegroup:
			queryset |= Movie.objects.filter(
				part__stationinmovie__station_service__pk=stationservicegroup.pk
			)

		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order')
		
		return organize_movie_query(queryset, sort, order)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		# 乗換駅を取得
		stationservice = StationService.objects.get(pk=self.kwargs['station_service'])
		stations = stationservice.station.get_group_station()
		transfers = {}
		if stations:
			for station in stations:
				transfers[station] = StationService.objects.filter(station=station)

		# 同一駅で、正式路線も同じものか判別
		# （山陽本線の岡山駅や、土讃線の高知駅など、ラインカラーが途中で変わる路線が主）
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