from django.db.models import Q
from pure_pagination.mixins import PaginationMixin
from django.views import generic
from django.shortcuts import render

from ..models import *

from .searchsets import *

def organize_movie_query(q, sort="published", order="newer"):
	"""
	sort,orderにより並べ替えを行う。
	sort -> published(投稿日時), view(再生回数)
	order -> older, newer(published), max, min(view)
	非アクティブな動画を除外し、一意にする
	"""

	q = q.exclude(is_active=False).order_by('-published_at').distinct()

	if sort == "published":

		if order == "older":
			q = q.order_by('published_at')
		elif order == "newer":
			q = q.order_by('-published_at')

	elif sort == "view":

		if order == "max":
			q = q.order_by('-n_view')
		elif order == "min":
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

		q_word = self.request.GET.get('word')
		if q_word:
			queryset = search_keyword(queryset, q_word)

		q_is_collab = self.request.GET.getlist('is_collab')
		if q_is_collab:
			queryset = search_is_collab(queryset, q_is_collab)

		q_channel = self.request.GET.get('channel')
		if q_channel:
			queryset = queryset.filter(channel__name__icontains=q_channel)

		q_sung_name = self.request.GET.get('sung_name')
		if q_sung_name:
			queryset = search_sung_name(queryset, q_sung_name)

		q_line_name_customize = self.request.GET.get('line_name_customize')
		if q_line_name_customize:
			queryset = search_line_name_customize(queryset, q_line_name_customize)

		q_song = self.request.GET.get('song')
		if q_song:
			queryset = search_song(queryset, q_song)

		q_artist = self.request.GET.get('artist')
		if q_artist:
			queryset = search_artist(queryset, q_artist)

		q_song_tag = self.request.GET.get('song_tag')
		if q_song_tag:
			queryset = search_song_tag(queryset, q_song_tag)

		q_published_at_start = self.request.GET.get('published_at_start')
		q_published_at_end = self.request.GET.get('published_at_end')
		if q_published_at_start and q_published_at_end:
			queryset = search_published_at(queryset, q_published_at_start, q_published_at_end)
			
		q_information_time_point_start = self.request.GET.get('information_time_point_start')
		q_information_time_point_end = self.request.GET.get('information_time_point_end')
		if q_information_time_point_start and q_information_time_point_end:
			queryset = search_information_time_point(queryset, q_information_time_point_start, q_information_time_point_end)
		

		return organize_movie_query(queryset, "published", "newer")


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		context['word'] = self.request.GET.get('word')
		context['is_collab'] = self.request.GET.getlist('is_collab')
		context['channel'] = self.request.GET.get('channel')
		context['sung_name'] = self.request.GET.get('sung_name')
		context['line_name_customize'] = self.request.GET.get('line_name_customize')
		context['song'] = self.request.GET.get('song')
		context['artist'] = self.request.GET.get('artist')
		context['song_tag'] = self.request.GET.get('song_tag')
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

	queryset = Movie.objects.all()

	movies = search_keyword(queryset, word)
	movies = organize_movie_query(movies)
	mcount = movies.count
	movies = movies[:5]

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

	movies_sungname = search_sung_name(queryset, word)
	movies_sungname = organize_movie_query(movies_sungname)
	sncount = movies_sungname.count
	movies_sungname = movies_sungname[:5]

	movies_song_tag = search_song_tag(queryset, word)
	movies_song_tag = organize_movie_query(movies_song_tag)
	tcount = movies_song_tag.count
	movies_song_tag = movies_song_tag[:5]

	movies_artist = search_artist(queryset, word)
	movies_artist = organize_movie_query(movies_artist)
	acount = movies_artist.count
	movies_artist = movies_artist[:5]

	movies_song = search_song(queryset, word)
	movies_song = organize_movie_query(movies_song)
	songcount = movies_song.count
	movies_song = movies_song[:5]

	context = {
		'movie_list': movies,
		"lineservices": lineservices,
		"stationservices": stationservices,
		"creators": creators,
		"movies_sungname": movies_sungname,
		"movies_songtag": movies_song_tag,
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

# class ArtistSearchView(PaginationMixin, generic.ListView):
# 	model = Movie
# 	paginate_by = 30
# 	template_name = 'moviedatabase/music/artistsearch.html'

# 	def get_queryset(self):
# 		queryset = super().get_queryset()

# 		queryset = Movie.objects.none()
# 		word = self.request.GET.get('word')

# 		if word:
# 			songnews = SongNew.objects.filter(Q(artist_name__icontains=word) | Q(artist_name_kana__icontains=word)).order_by('artist_name_kana')
			
# 			for song in songnews:
# 				queryset |= Movie.objects.filter(songnew=song)
# 				parts = Part.objects.filter(songnew=song)
# 				for part in parts:
# 					queryset |= Movie.objects.filter(pk=part.movie.pk)
		
# 		return organize_movie_query(queryset)

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
		
# 		word = self.request.GET.get('word')
# 		context['word'] = word

# 		return context

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
		return organize_movie_query(queryset, sort, order)

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
		return organize_movie_query(queryset, sort, order)

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
		return organize_movie_query(queryset, sort, order)

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
		return organize_movie_query(queryset, sort, order)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		niconico = NiconicoAccount.objects.get(pk=self.kwargs['niconico_account'])
		
		context['niconico'] = niconico

		context['sort'] = self.request.GET.get('sort')
		context['order'] = self.request.GET.get('order')

		return context