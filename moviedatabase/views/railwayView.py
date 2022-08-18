from django.views import generic
from ..models import *

from pure_pagination.mixins import PaginationMixin
from django.db.models import Q

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
		
		movies = lineinmovies.values_list('part__movie__pk', flat=True)
		for movie in movies:
			queryset |= Movie.objects.filter(pk=movie)

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
		
		movies = stationinmovies.values_list('part__movie__pk', flat=True)
		for movie in movies:
			queryset |= Movie.objects.filter(pk=movie)
			
		stationservicegroup = stationservice.get_group_station_service()
		if stationservicegroup:
			if stationservicegroup.station.line == stationservice.station.line:
				stationinmovies = StationInMovie.objects.filter(station_service=stationservice)
				movies = stationinmovies.values_list('part__movie__pk', flat=True)
				for movie in movies:
					queryset |= Movie.objects.filter(pk=movie)

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