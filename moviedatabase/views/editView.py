from pip import main
from ..models import *
from .. import forms

from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.mixins import PermissionRequiredMixin

import pytz

# requestしたuserがmain_idの動画を編集する権限があるか確認
def can_edit_movie(request, main_id):
	channels = request.user.all_can_edit_channel()
	movie = Movie.objects.get(main_id=main_id)
	if not movie:
		return False

	flag = False

	for channel in channels:
		if (channel == movie.channel):
			flag = True

	return flag

# 編集履歴（詳細）を保存
def add_updatehistory(request, main_id, category):
	movie = Movie.objects.get(main_id=main_id)
	history = UpdateHistory(movie=movie, user=request.user, reg_date=timezone.now(), category=category)
	history.save()

# 編集履歴（トップページ情報）を保存
def add_updateinformation(request, main_id):
	movie = get_object_or_404(Movie, main_id=main_id)
	info = MovieUpdateInformation.objects.filter(movie=movie)
	type = 'U' if (info) else 'C'
	new_info = MovieUpdateInformation(movie=movie, creator=None, is_create=type, user=request.user, reg_date=timezone.now())
	new_info.save()

	movie.update_date = timezone.now()
	movie.save()

# YouTube情報を更新できるか判定（1日に1回更新可能）
def is_can_statistics_update(movie):
	JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
	now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
	day = datetime.datetime(now.year, now.month, now.day, 0, 0, tzinfo=JST)
	return day > movie.statistics_update_date
	# trueなら更新可能


# 新規動画登録
class MovieRegisterView(PermissionRequiredMixin, generic.CreateView):
	template_name = 'moviedatabase/register.html'
	model = Movie
	form_class = forms.MovieRegisterForm
	permission_required = ('moviedatabase.add_movie')

	# Formクラスにrequestの中身を受け渡す（userの登録できるチャンネル判別用）
	def get_form_kwargs(self):
		kw = super(MovieRegisterView, self).get_form_kwargs()
		kw['request'] = self.request
		return kw
		
	def get_success_url(self):
		return reverse_lazy('moviedatabase:movie_edit', kwargs={'main_id': self.object.main_id})


# YouTube情報更新
@permission_required('moviedatabase.add_movie')
def movie_statistics_update(request, main_id):
	
	if not can_edit_movie(request, main_id):
		return redirect('moviedatabase:login')
		
	add_updatehistory(request, main_id, 'access-statistics-update')

	movie = get_object_or_404(Movie, main_id=main_id)

	can_statistics_update = is_can_statistics_update(movie)
	if not can_statistics_update:
		return render(request, '403.html')	

	form = forms.MovieStatisticsUpdateForm(request.POST or None, instance=movie)
	if request.method == 'POST' and form.is_valid():
		form.save()
		add_updatehistory(request, main_id, 'complete-statistics-update')
		return redirect('moviedatabase:detail', main_id=main_id)

	context = {
		'movie': movie,
		'form': form
	}

	return render(request, 'moviedatabase/movie_statistics_update.html', context)


# 動画情報編集
@permission_required('moviedatabase.add_movie')
def movie_edit(request, main_id):

	if not can_edit_movie(request, main_id):
		return redirect('moviedatabase:login')

	add_updatehistory(request, main_id, 'access-movie-edit')

	movie = get_object_or_404(Movie, main_id=main_id)
	form = forms.MovieUpdateForm(request.POST or None, instance=movie)
	parts = Part.objects.filter(movie=main_id)
	partcount = parts.count()

	if request.method == 'POST' and form.is_valid():
		form.save()

		# 単作として登録ボタンをクリックした場合
		if (partcount == 0) and ('single' in request.POST):
			new_single_part = Part.objects.create(
				sort_by_movie="0",
				short_name="0",
				name="",
				movie=movie,
				start_time=datetime.timedelta(0)
			)
			
			# 動画全体の参加者・楽曲をパートにも登録
			new_single_part.participant.add(movie.channel.main_name)
			songs = movie.songnew.all()
			for song in songs:
				new_single_part.songnew.add(song)
			
			return redirect('moviedatabase:station_edit', main_id=main_id, sort_by_movie=0)
		
		# パートが1つだけ存在する場合（既に登録している単作扱い）
		elif partcount == 1:
			first_part = parts.first()
			return redirect('moviedatabase:station_edit', main_id=main_id, sort_by_movie=first_part.sort_by_movie)
		
		# パートが複数存在する場合（既に登録している合作扱い）
		else:
			return redirect('moviedatabase:part_edit', main_id=main_id)

	context = {
		'movie': movie,
		'form': form,
		'parts': parts,
		'partcount': partcount
	}

	return render(request, 'moviedatabase/movie_edit.html', context)


# パート情報編集
@permission_required('moviedatabase.add_part')
def movie_part_edit(request, main_id):

	if not can_edit_movie(request, main_id):
		return redirect('moviedatabase:login')

	add_updatehistory(request, main_id, 'access-part-edit')

	movie = get_object_or_404(Movie, main_id=main_id)
	form = forms.MovieUpdateForm(request.POST or None, instance=movie)
	formset = forms.PartEditFormset(request.POST or None, instance=movie)
	
	if request.method == 'POST' and form.is_valid() and formset.is_valid():
		form.save()
		formset.save()

		first_part = Part.objects.filter(movie=main_id).order_by('sort_by_movie').first()
		if first_part:
			# パートが存在する場合（1つでも複数でも）
			return redirect('moviedatabase:station_edit', main_id=main_id, sort_by_movie=first_part.sort_by_movie)
		else:
			# パートが登録されていない場合
			return redirect('moviedatabase:detail', main_id=main_id)

	context = {
		'movie': movie,
		'form': form,
		'formset': formset
	}

	return render(request, 'moviedatabase/part_edit.html', context)

# 駅情報編集
@permission_required('moviedatabase.add_stationinmovie')
def movie_part_station_edit(request, main_id, sort_by_movie):

	if not can_edit_movie(request, main_id):
		return redirect('moviedatabase:login')

	add_updatehistory(request, main_id, 'access-part-station-edit')

	part = get_object_or_404(Part, movie=main_id, sort_by_movie=sort_by_movie)

	# 「情報の日付」欄にデフォルトで入れる日付
	original_date = datetime.date(part.movie.published_at_year, part.movie.published_at_month, part.movie.published_at_day)
	information_time_point = original_date if (part.information_time_point is None) else part.information_time_point
	initial_dict = {
		'information_time_point': information_time_point,
	}
	
	part_form = forms.PartEditForm(request.POST or None, instance=part, initial=initial_dict)
	formset = forms.StationInMovieEditFormset(request.POST or None, instance=part)
	
	if request.method == 'POST' and part_form.is_valid() and formset.is_valid():
		part_form.save()
		formset.save()

		stations = StationInMovie.objects.filter(part=part)
		lines = LineService.objects.none()

		for station in stations:
			# カスタマイズ路線名が空欄だった場合、元の駅オブジェクトの路線名を追加
			if (station.line_name_customize is None or station.line_name_customize == ""):
				station.line_name_customize = station.station_service.line_service.__str__()
				station.save()
			# パート路線リストに各駅の路線情報を追加
			lines |= LineService.objects.filter(pk=station.station_service.line_service.pk)
		
		lineinmovies = []
		# パート路線リストからLineInMovieオブジェクトを生成する準備。（路線検索の高速化を図る）
		for line in lines:
			lineinmovie = LineInMovie(part=part, line_service=line)
			lineinmovies.append(lineinmovie)

		# もともと紐づいていたLineInMovieオブジェクトを消去し、新たに生成
		LineInMovie.objects.filter(part=part).delete()
		LineInMovie.objects.bulk_create(lineinmovies)

		next_part = Part.objects.filter(movie=main_id, sort_by_movie=sort_by_movie+1)
		if next_part.first() is None:
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

# 編集内容確認
@permission_required('moviedatabase.add_movie')
def confirm_movie(request, main_id):

	if not can_edit_movie(request, main_id):
		return redirect('moviedatabase:login')

	add_updatehistory(request, main_id, 'access-confirm')

	movie = get_object_or_404(Movie, main_id=main_id)
	parts = Part.objects.filter(movie=movie).order_by('sort_by_movie')
	
	onlyonepart = True if (parts.count() == 1) else False

	can_edit = request.user.groups.filter(name='can_edit').exists()

	context = {
		'movie': movie,
		'parts': parts,
		'onlyonepart': onlyonepart,
		'can_edit': can_edit,
		'type': "confirm"
	}

	return render(request, 'moviedatabase/detail.html', context)

# 動画詳細画面（全体公開ページ）
def detail_movie(request, main_id):
	movie = get_object_or_404(Movie, main_id=main_id)
	parts = Part.objects.filter(movie=movie).order_by('sort_by_movie')
	if parts.count() == 1:
		onlyonepart = True
	else:
		onlyonepart = False

	can_edit = request.user.groups.filter(name='can_edit').exists()
	can_edit = can_edit and can_edit_movie(request, main_id)

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
		add_updateinformation(request, main_id)

	context = {
		'movie': movie,
		'parts': parts,
		'onlyonepart': onlyonepart,
		'can_edit': can_edit,
		'can_statistics_update': is_can_statistics_update(movie),
		'type': "detail"
	}

	return render(request, 'moviedatabase/detail.html', context)