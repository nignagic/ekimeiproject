from django.db.models import Q
from pure_pagination.mixins import PaginationMixin
from django.views import generic
from django.shortcuts import render

from ..models import *

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