from django.db.models import Q, Prefetch

from ..models import *

def organize_movie_query(query, sort="published", order="newer"):
	"""
	sort,orderにより並べ替えを行う。
	sort -> published(投稿日時), view(再生回数)
	order -> older, newer(published), max, min(view)
	非アクティブな動画を除外し、一意にする
	"""

	query = query.exclude(is_active=False).order_by('-published_at').distinct()

	if sort == "published":

		if order == "older":
			query = query.order_by('published_at')
		elif order == "newer":
			query = query.order_by('-published_at')

	elif sort == "view":

		if order == "max":
			query = query.order_by('-n_view')
		elif order == "min":
			query = query.order_by('n_view')

	return query

def search_keyword(queryset, word):
    if word is None:
        return Movie.objects.none()

    movie_queryset = queryset.filter(
        Q(title__icontains=word) | 
        Q(main_id__icontains=word) |
        Q(description__icontains=word) | 
        Q(explanation__icontains=word) |
        Q(part__name__icontains=word) | 
        Q(part__explanation__icontains=word)
    ).distinct()

    return movie_queryset


def search_is_collab(queryset, q_is_collab):
    if q_is_collab is None:
        return Movie.objects.none()

    movies_is_collab = Movie.objects.none()

    for q in q_is_collab:
        movies_is_collab |= queryset.filter(is_collab=q)

    return movies_is_collab


def search_sung_name(queryset, q_sung_name):
    if q_sung_name is None:
        return Movie.objects.none()

    movies_sung_name = queryset.filter(
        part__stationinmovie__sung_name__icontains=q_sung_name
    ).distinct()
    
    return movies_sung_name


def search_line_name_customize(queryset, q_line_name_customize):
    if q_line_name_customize is None:
        return Movie.objects.none()

    movies_linenamecustomize = queryset.filter(
        part__stationinmovie__line_name_customize__icontains=q_line_name_customize
    ).distinct()
      
    return movies_linenamecustomize


def search_song(queryset, q_song):
    if q_song is None:
        return Movie.objects.none()

    movies_song = queryset.filter(
        Q(songnew__song_name__icontains=q_song) | 
        Q(songnew__song_name_kana__icontains=q_song) |
        Q(part__songnew__song_name__icontains=q_song) | 
        Q(part__songnew__song_name_kana__icontains=q_song)
    ).distinct()

    return movies_song


def search_artist(queryset, q_artist):
    if q_artist is None:
        return Movie.objects.none()
        
    movies_artist = queryset.filter(
        Q(songnew__artist_name__icontains=q_artist) | 
        Q(songnew__artist_name_kana__icontains=q_artist) |
        Q(part__songnew__artist_name__icontains=q_artist) | 
        Q(part__songnew__artist_name_kana__icontains=q_artist)
    ).distinct()

    return movies_artist


def search_song_tag(queryset, q_song_tag):
    if q_song_tag is None:
        return Movie.objects.none()
        
    movies_song_tag = queryset.filter(
        Q(songnew__tag__icontains=q_song_tag) |
        Q(part__songnew__tag__icontains=q_song_tag)
    ).distinct()

    return movies_song_tag


def search_published_at(queryset, q_published_at_start, q_published_at_end):
    if q_published_at_start is None or q_published_at_end is None:
        return Movie.objects.none()
        
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

    q_published_at_start = datetime.datetime.strptime(q_published_at_start, '%Y-%m-%dT%H:%M').astimezone(JST)
    q_published_at_end = datetime.datetime.strptime(q_published_at_end, '%Y-%m-%dT%H:%M').astimezone(JST)
    
    movies_published_at = queryset.filter(
        published_at__gte=q_published_at_start, 
        published_at__lte=q_published_at_end
    ).distinct()

    return movies_published_at


def search_information_time_point(queryset, q_information_time_point_start, q_information_time_point_end):
    if q_information_time_point_start is None or q_information_time_point_end is None:
        return Movie.objects.none()
        
    movies_infotime = queryset.filter(
        part__information_time_point__gte=q_information_time_point_start, 
        part__information_time_point__lte=q_information_time_point_end
    ).distinct()

    return movies_infotime