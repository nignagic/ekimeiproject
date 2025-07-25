from django.conf import settings

from django.db import models
from stationdata.models import *
from songdata.models import *
from user.models import *
import datetime

# Create your models here.
class Creator(models.Model):
	name = models.CharField('作者名', max_length=200)
	name_kana = models.CharField('読み', max_length=200)

	class Meta:
		ordering = ['name_kana', 'name']

	def __str__(self):
		return self.name

class Name(models.Model):
	name = models.CharField('名義', max_length=200)
	creator = models.ForeignKey(Creator, null=True, blank=True, on_delete=models.SET_NULL, related_name='creator_name', verbose_name='作者')
	
	class Meta:
		ordering = ['creator', 'name']

	def __str__(self):
		return self.name

class YoutubeChannel(models.Model):
	name = models.CharField('YouTubeチャンネル名', max_length=200)
	channel_id = models.CharField(max_length=200, primary_key=True)
	icon = models.CharField(max_length=200, blank=True, null=True)
	creator = models.ForeignKey(Creator, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='作者')
	main_name = models.ForeignKey(Name, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='チャンネル名義')
	is_main = models.BooleanField('メインチャンネル', default=True)
	
	class Meta:
		ordering = ['creator', '-is_main']

	def __str__(self):
		return self.name

class NiconicoAccount(models.Model):
	name = models.CharField('niconicoアカウント名', max_length=200)
	user_id = models.CharField(max_length=200, primary_key=True)
	creator = models.ForeignKey(Creator, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='作者')
	is_main = models.BooleanField('メインアカウント', default=True)
	def __str__(self):
		return self.name

class TwitterAccount(models.Model):
	name = models.CharField('名前', null=True, blank=True, max_length=200)
	user_id = models.CharField(max_length=200, primary_key=True)
	creator = models.ForeignKey(Creator, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='作者')
	is_main = models.BooleanField('メインアカウント', default=True)
	def __str__(self):
		return "@" + self.user_id

class PageLink(models.Model):
	name = models.CharField('リンク名', null=True, blank=True, max_length=200)
	url = models.CharField('URL', null=True, blank=True, max_length=200)
	creator = models.ForeignKey(Creator, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='作者')
	def __str__(self):
		return self.url

class MovieCategory(models.Model):
	name = models.CharField('動画カテゴリー', max_length=200)
	object_name = models.CharField('歌唱オブジェクト名', max_length=200, null=True, blank=True)
	def __str__(self):
		return self.name

class Movie(models.Model):
	title = models.CharField('動画タイトル', max_length=400)
	channel = models.ForeignKey(
		YoutubeChannel, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='投稿チャンネル'
	)
	niconico_account = models.ForeignKey(
		NiconicoAccount, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='投稿ニコニコアカウント'
	)
	main_id = models.CharField('動画ID', max_length=200, unique=True)
	youtube_id = models.CharField('YouTube 動画ID', max_length=200, null=True, blank=True)
	niconico_id = models.CharField('ニコニコ動画 動画ID', max_length=200, null=True, blank=True)
	
	published_at = models.DateTimeField('投稿日時', null=True, blank=True)
	published_at_year = models.IntegerField('投稿日時[日本時間]（年）', null=True, blank=True)
	published_at_month = models.IntegerField('投稿日時[日本時間]（月）', null=True, blank=True)
	published_at_day = models.IntegerField('投稿日時[日本時間]（日）', null=True, blank=True)
	published_at_hour = models.IntegerField('投稿日時[日本時間]（時）', null=True, blank=True)
	published_at_minute = models.IntegerField('投稿日時[日本時間]（分）', null=True, blank=True)
	published_at_second = models.IntegerField('投稿日時[日本時間]（秒）', null=True, blank=True)

	duration = models.DurationField('長さ', null=True, blank=True)
	n_view = models.IntegerField('再生回数', default=0, null=True, blank=True)
	n_like = models.IntegerField('高評価数', default=0, null=True, blank=True)
	n_dislike = models.IntegerField('低評価数', default=0, null=True, blank=True)
	n_comment = models.IntegerField('コメント数', default=0, null=True, blank=True)
	description = models.TextField('説明', null=True, blank=True)

	reg_date = models.DateTimeField('データベース登録日時', null=True, blank=True)
	update_date = models.DateTimeField('データベース更新日時', null=True, blank=True)
	statistics_update_date = models.DateTimeField('統計情報更新日時', null=True, blank=True)

	song = models.ManyToManyField(Song, blank=True, verbose_name='使用楽曲(動画全体)(旧)')
	songnew = models.ManyToManyField(SongNew, blank=True, verbose_name='使用楽曲(楽曲全体)', related_name='movie')
	# vocal = models.ManyToManyField(Vocal, blank=True, verbose_name='使用ボーカル(動画全体)')
	vocalnew = models.ManyToManyField(VocalNew, blank=True, verbose_name='使用ボーカル(動画全体)')

	COLLAB = (
		('S', '単作'),
		('C', '合作')
	)
	is_collab = models.CharField('単作or合作', max_length=1, choices=COLLAB, default='S')
	parent = models.ManyToManyField('self', blank=True, verbose_name='親作品')
	related = models.ManyToManyField('self', blank=True, verbose_name='関連作品')
	explanation = models.TextField('補足説明', blank=True)
	is_active = models.BooleanField('active', default=True)
	class Meta:
		ordering = ['-published_at']

	def category(self):
		parts = Part.objects.filter(movie=self.main_id)
		text = []
		for part in parts:
			categories = part.get_complex_category()
			if categories:
				for c in categories:
					text.append(c)
		return list(set(text))

	def get_duration(self):
		d = self.duration
		d = str(d).split(':')
		if d[0] != "0":
			if d[0][0] == "0":
				d[0] = d[0][1]
			return d[0] + ":" + d[1] + ":" + d[2]
		else:
			if d[1][0] == "0":
				d[1] = d[1][1]
			return d[1] + ":" + d[2]

	def __str__(self):
		return self.title

class Part(models.Model):
	sort_by_movie = models.IntegerField()
	short_name = models.CharField(max_length=10, null=True, blank=True)
	name = models.CharField('パート名', max_length=200, null=True, blank=True)
	movie = models.ForeignKey(Movie, to_field='main_id', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='動画', related_name='part')
	participant = models.ManyToManyField(Name, blank=True, verbose_name='参加名義')
	category = models.ForeignKey(MovieCategory, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='カテゴリー')
	start_time = models.DurationField('開始時間', null=True, blank=True, default='00:00:00')
	song = models.ManyToManyField(Song, blank=True, verbose_name='使用楽曲(パート)(旧)')
	songnew = models.ManyToManyField(SongNew, blank=True, verbose_name='使用楽曲(パート)', related_name='part')
	# vocal = models.ManyToManyField(Vocal, blank=True, verbose_name='使用ボーカル(パート)')
	vocalnew = models.ManyToManyField(VocalNew, blank=True, verbose_name='使用ボーカル(パート)')
	explanation = models.TextField('補足説明', null=True, blank=True)
	incomplete = models.BooleanField('情報が不完全', default=False)
	
	information_time_point = models.DateField('情報の日付', null=True, blank=True)

	complex_category = models.TextField('複合カテゴリー', blank=True)

	def get_complex_category(self):
		s = self.complex_category.split('\n')
		return s

	def part_num(self):
		return self.sort_by_movie + 1;

	def movie_publish_date(self):
		return datetime.date(self.movie.published_at_year, self.movie.published_at_month, self.movie.published_at_day)

	def __str__(self):
		if self.name:
			n = self.name
		elif self.short_name:
			n = self.short_name
		else:
			n = "#" + str(self.sort_by_movie+1)

		if self.movie:
			return "【" + n + "】" + self.movie.title
		else:
			return n

class StationInMovie(models.Model):
	sort_by_part = models.IntegerField()
	part = models.ForeignKey(Part, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='動画パート', related_name='stationinmovie')
	station_service = models.ForeignKey(StationService, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='駅')
	line_service_on_other_options = models.ForeignKey(LineService, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='路線（その他の駅用）')
	line_name_customize = models.CharField('所属路線名カスタマイズ', null=True, blank=True, max_length=200)
	sung_name = models.CharField('歌唱名', null=True, blank=True, max_length=400)
	back_rel = models.IntegerField('前駅との関係', default=1)
	explanation = models.TextField('補足説明', null=True, blank=True)
	def get_line_service(self):
		if (self.line_service_on_other_options and self.station_service.line_service.company.other_option):
			return self.line_service_on_other_options
		return self.station_service.line_service

	def get_line_name(self):
		if (self.line_name_customize == ""):
			return self.station_service.line_service.__str__
		if (self.line_name_customize != self.station_service.line_service.__str__):
			return self.line_name_customize
		return self.station_service.line_service.__str__

	def __str__(self):
		return self.sung_name

class LineInMovie(models.Model):
	part = models.ForeignKey(Part, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='動画パート')
	line_service = models.ForeignKey(LineService, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='路線')
	def __str__(self):
		if self.line_service:
			return self.line_service.name
		else:
			return "object"

class MovieUpdateInformation(models.Model):
	movie = models.ForeignKey(Movie, to_field='main_id', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='動画')
	creator = models.ForeignKey(Creator, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='作者')

	INFO_TYPE = (
		('C', '新規登録'),
		('U', '更新')
	)
	is_create = models.CharField('新規登録か更新か', max_length=1, choices=INFO_TYPE, default='C')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='編集者')
	reg_date = models.DateTimeField('登録・更新日時', blank=True)
	class Meta:
		ordering = ['-reg_date']

	def __str__(self):
		if self.movie:
			return self.movie.title + " - " + self.get_is_create_display()
		elif self.creator:
			return self.creator.name + " - " + self.get_is_create_display()
		else:
			return "info"

	def text(self):
		if self.movie:
			return "「" + self.movie.title + "」を" + self.get_is_create_display() + "しました。"
		elif self.creator:
			return "「" + self.creator.name + "」を" + self.get_is_create_display() + "しました。"
		else:
			return "Information"

class NoticeInformation(models.Model):
	reg_date = models.DateTimeField('日時', blank=True)
	category = models.CharField('種類', null=True, blank=True, max_length=100)
	head = models.CharField('概要', null=True, blank=True, max_length=100)
	text = models.TextField('説明', null=True, blank=True)
	class Meta:
		ordering = ['-reg_date']

	def __str__(self):
		return self.head

class UpdateHistory(models.Model):
	movie = models.ForeignKey(Movie, to_field='main_id', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='動画')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='編集者')
	reg_date = models.DateTimeField('登録・更新日時', blank=True)
	category = models.CharField('種別', null=True, blank=True, max_length=100)
	class meta:
		ordering = ['-reg_date']
			
	def __str__(self):
		n = self.user.username if self.user else ""
		c = "[" + self.category + "]" if self.category else ""
		if self.movie:
			return self.movie.title + " - " + n + c
		else:
			return "info"

class AccountAndCreatorApplication(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='編集者')
	creator = models.ForeignKey(Creator, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='作者')
	reg_date = models.DateTimeField('登録・更新日時', blank=True)
	dealing = models.CharField('動画の扱い', null=True, blank=True, max_length=200)
	class meta:
		ordering = ['-reg_date']

	def __str__(self):
		n = ""
		if self.user:
			n += self.user.username
		if self.creator:
			n += " " + self.creator.name
		return n

class TopImage(models.Model):
	file_name = models.CharField('ファイル名', null=True, blank=True, max_length=200)
	text = models.TextField('説明', null=True, blank=True)
	is_active = models.BooleanField('active', default=True)
	def __str__(self):
		return self.file_name