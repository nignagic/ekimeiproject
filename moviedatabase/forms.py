from django.forms import Form, ModelForm, inlineformset_factory
from django import forms
from .models import *

from django.contrib.auth.forms import (
	AuthenticationForm
)

class LoginForm(AuthenticationForm):
	"""ログインフォーム"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

class MovieRegisterForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ('title', 'channel', 'main_id', 'youtube_id', 'niconico_id', 'published_at', 'duration', 'n_view', 'n_like', 'n_dislike', 'n_comment', 'description', 'reg_date', 'statistics_update_date')
		widgets = {
			'title': forms.HiddenInput(attrs={
				'class': 'title',
			}),
			'channel': forms.HiddenInput(attrs={
				'id': 'channel',
			}),
			'main_id': forms.HiddenInput(attrs={
				'class': 'main_id',
			}),
			'youtube_id': forms.HiddenInput(attrs={
				'class': 'youtube_id',
			}),
			'niconico_id': forms.HiddenInput(attrs={
				'class': 'niconico_id',
			}),
			'published_at': forms.HiddenInput(attrs={
				'class': 'published_at',
			}),
			'duration': forms.HiddenInput(attrs={
				'class': 'duration',
			}),
			'n_view': forms.HiddenInput(attrs={
				'class': 'n_view',
			}),
			'n_like': forms.HiddenInput(attrs={
				'class': 'n_like',
			}),
			'n_dislike': forms.HiddenInput(attrs={
				'class': 'n_dislike',
			}),
			'n_comment': forms.HiddenInput(attrs={
				'class': 'n_comment',
			}),
			'description': forms.HiddenInput(attrs={
				'class': 'description',
			}),
			'reg_date': forms.HiddenInput(attrs={
				'class': 'reg_date',
			}),
			'statistics_update_date': forms.HiddenInput(attrs={
				'class': 'statistics_update_date',
			}),
		}
		labels = {
			'title': '',
			'channel': '',
			'main_id': '',
			'youtube_id': '',
			'niconico_id': '',
			'published_at': '',
			'duration': '',
			'n_view': '',
			'n_like': '',
			'n_dislike': '',
			'n_comment': '',
			'description': '',
			'reg_date': '',
			'statistics_update_date': '',
		}
		error_messages = {
			'title': {
				'required': 'タイトルが適切に入力されていません'
			},
			'main_id': {
				'required': '動画IDが適切に入力されていません',
			},
			'channel': {
				'invalid_choice': 'この動画のチャンネルはデータベース上の登録対象外です'
			}
		}

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request')
		super(MovieRegisterForm, self).__init__(*args, **kwargs)

	def clean(self):
		channel = self.cleaned_data['channel']
		cs = self.request.user.all_can_edit_channel()
		flag = False
		for c in cs:
			if (c == channel):
				flag = True

		if not flag:
			raise forms.ValidationError("このチャンネルの動画はログイン中のユーザーでは登録できません")

		if Movie.objects.filter(main_id=self.cleaned_data['main_id']).exists():
			raise forms.ValidationError("この動画は既にデータベース上に存在しています。")

class MovieStatisticsUpdateForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ('title', 'channel', 'main_id', 'youtube_id', 'niconico_id', 'published_at', 'duration', 'n_view', 'n_like', 'n_dislike', 'n_comment', 'description', 'statistics_update_date')
		widgets = {
			'title': forms.HiddenInput(attrs={
				'class': 'title',
			}),
			'channel': forms.HiddenInput(attrs={
				'id': 'channel',
			}),
			'main_id': forms.HiddenInput(attrs={
				'class': 'main_id',
			}),
			'youtube_id': forms.HiddenInput(attrs={
				'class': 'youtube_id',
			}),
			'niconico_id': forms.HiddenInput(attrs={
				'class': 'niconico_id',
			}),
			'published_at': forms.HiddenInput(attrs={
				'class': 'published_at',
			}),
			'duration': forms.HiddenInput(attrs={
				'class': 'duration',
			}),
			'n_view': forms.HiddenInput(attrs={
				'class': 'n_view',
			}),
			'n_like': forms.HiddenInput(attrs={
				'class': 'n_like',
			}),
			'n_dislike': forms.HiddenInput(attrs={
				'class': 'n_dislike',
			}),
			'n_comment': forms.HiddenInput(attrs={
				'class': 'n_comment',
			}),
			'description': forms.HiddenInput(attrs={
				'class': 'description',
			}),
			'statistics_update_date': forms.HiddenInput(attrs={
				'class': 'statistics_update_date',
			}),
		}
		labels = {
			'title': '',
			'channel': '',
			'main_id': '',
			'youtube_id': '',
			'niconico_id': '',
			'published_at': '',
			'duration': '',
			'n_view': '',
			'n_like': '',
			'n_dislike': '',
			'n_comment': '',
			'description': '',
			'statistics_update_date': '',
		}
		error_messages = {
			'title': {
				'required': 'タイトルが適切に入力されていません'
			},
			'main_id': {
				'required': '動画IDが適切に入力されていません',
			},
			'channel': {
				'invalid_choice': 'この動画のチャンネルはデータベース上の登録対象外です'
			}
		}

class MovieUpdateForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ('title', 'channel', 'main_id', 'youtube_id', 'niconico_id', 'published_at', 'duration', 'n_view', 'n_like', 'n_dislike', 'n_dislike', 'n_comment', 'description', 'reg_date', 'songnew', 'is_collab', 'parent', 'related', 'explanation', 'is_active')
		widgets = {
			'title': forms.HiddenInput(attrs={
				'class': 'title',
			}),
			'channel': forms.HiddenInput(attrs={
				'id': 'channel',
			}),
			'main_id': forms.HiddenInput(attrs={
				'class': 'main_id',
			}),
			'youtube_id': forms.HiddenInput(attrs={
				'class': 'youtube_id',
			}),
			'niconico_id': forms.HiddenInput(attrs={
				'class': 'niconico_id',
			}),
			'published_at': forms.HiddenInput(attrs={
				'class': 'published_at',
			}),
			'duration': forms.HiddenInput(attrs={
				'class': 'duration',
			}),
			'n_view': forms.HiddenInput(attrs={
				'class': 'n_view',
			}),
			'n_like': forms.HiddenInput(attrs={
				'class': 'n_like',
			}),
			'n_dislike': forms.HiddenInput(attrs={
				'class': 'n_dislike',
			}),
			'n_comment': forms.HiddenInput(attrs={
				'class': 'n_comment',
			}),
			'description': forms.HiddenInput(attrs={
				'class': 'description',
			}),
			'reg_date': forms.HiddenInput(attrs={
				'class': 'reg_date',
			}),
			'is_collab': forms.RadioSelect(),
			'songnew': forms.MultipleHiddenInput(attrs={
				'class': 'selected_song_in_movie',
			}),
			'parent': forms.MultipleHiddenInput(attrs={
				'class': 'selected_parent_movie',
			}),
			'related': forms.MultipleHiddenInput(attrs={
				'class': 'selected_related_movie',
			}),
		}

class PartEditFormforinline(forms.ModelForm):
	class Meta:
		model = Part
		fields = ('sort_by_movie', 'short_name', 'name', 'movie', 'participant', 'start_time', 'songnew', 'explanation')
		widgets = {
			'sort_by_movie': forms.HiddenInput(attrs={
				'class': 'sort_by_movie',
			}),
			'short_name': forms.TextInput(attrs={
				'class': 'short_name',
			}),
			'name': forms.TextInput(attrs={
				'class': 'part_name',
			}),
			'movie': forms.HiddenInput(attrs={
				'class': 'part_movie',
			}),
			'participant': forms.MultipleHiddenInput(attrs={
				'class': 'part_participant',
			}),
			'start_time': forms.TextInput(attrs={
				'class': 'start_time',
			}),
			'songnew': forms.MultipleHiddenInput(attrs={
				'class': 'part_song',
			}),
			'explanation': forms.HiddenInput(attrs={
				'class': 'part_explanation',
			}),
		}

	def __init__(self, *args, **kwargs):
		super(PartEditFormforinline, self).__init__(*args, **kwargs)
		self.fields['short_name'].error_messages = {'required': 'パート番号を入力するか、削除してください'}

PartEditFormset = forms.inlineformset_factory(
	parent_model = Movie,
	model = Part,
	form = PartEditFormforinline,
	extra = 0,
	can_delete = True,
	can_order = True
)

class PartEditForm(forms.ModelForm):
	class Meta:
		model = Part
		fields = ('name', 'movie', 'participant', 'category', 'start_time', 'songnew', 'vocalnew', 'explanation', 'incomplete')
		widgets = {
			'name': forms.TextInput(attrs={
				'class': 'name',
			}),
			'movie': forms.HiddenInput(attrs={
				'class': 'movie',
			}),
			'participant': forms.MultipleHiddenInput(attrs={
				'class': 'selected_participant',
			}),
			'category': forms.Select(attrs={
				'class': 'category',
			}),
			'start_time': forms.TextInput(attrs={
				'class': 'start_time',
			}),
			'songnew': forms.MultipleHiddenInput(attrs={
				'class': 'selected_song_in_part',
			}),
			'vocalnew': forms.MultipleHiddenInput(attrs={
				'class': 'selected_vocalnew',
			}),
			'explanation': forms.TextInput(attrs={
				'class': 'explanation',
			}),
		}

class StationInMovieEditForm(forms.ModelForm):
	BACKREL_CHOICES = [
		(0, '強制的につなげる'),
		(1, '通常接続'),
		(2, '強制的に離す'),
	]
	back_rel = forms.ChoiceField(
		label='前駅関係', choices=BACKREL_CHOICES, widget=forms.Select
	)
	class Meta:
		model = StationInMovie
		fields = ('sort_by_part', 'part', 'station_service', 'sung_name', 'back_rel', 'explanation')
		widgets = {
			'sort_by_part': forms.HiddenInput(attrs={
				'class': 'sort_by_part',
			}),
			'part': forms.Select(attrs={
				'class': 'part',
			}),
			'station_service': forms.HiddenInput(attrs={
				'class': 'station_service',
			}),
			'sung_name': forms.TextInput(attrs={
				'class': 'sung_name',
			}),
			'back_rel': forms.TextInput(attrs={
				'class': 'back_rel',
			}),
			'explanation': forms.TextInput(attrs={
				'class': 'explanation',
			})
		}

StationInMovieEditFormset = forms.inlineformset_factory(
	parent_model = Part,
	model = StationInMovie,
	form = StationInMovieEditForm,
	extra = 0,
	can_delete = True
)