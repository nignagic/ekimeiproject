from django.conf import settings
from django.db import models

import re
import jaconv

# Create your models here.
def initial_ex(s):
	if re.compile(r'[\u3041-\u3096]').search(s[0]):
		s = jaconv.hira2hkata(s)
	elif re.compile(r'[\u30A0-\u30FA]').search(s[0]):
		s = jaconv.z2h(s)
	s = jaconv.h2z(s[0])
	return s

class Artist(models.Model):
	name = models.CharField('アーティスト名', max_length=200)
	name_kana = models.CharField('アーティスト名カナ', max_length=200, null=True, blank=True)
	parent = models.ManyToManyField('self', blank=True, verbose_name='所属グループ等')
	related = models.ManyToManyField('self', blank=True, verbose_name='関連アーティスト')
	cv = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='担当声優')
	class Meta:
		ordering = ('name_kana', 'name')

	def initial(self):
		if self.name_kana:
			return initial_ex(self.name_kana[0])
		else:
			return "a"

	def __str__(self):
		return self.name

class Song(models.Model):
	name = models.CharField('曲名', max_length=200)
	name_kana = models.CharField('曲名カナ', max_length=200, null=True, blank=True)
	artist = models.ManyToManyField(Artist, blank=True, verbose_name='アーティスト')
	tieup = models.CharField('タイアップ等', max_length=400, null=True, blank=True)
	description = models.TextField('説明', max_length=500, null=True, blank=True)
	parent = models.ManyToManyField('self', blank=True, verbose_name='原作等')
	original = models.CharField('原作URL', max_length=200, null=True, blank=True)
	class Meta:
		ordering = ('name_kana', 'name')

	def initial(self):
		if self.name_kana:
			return self.name_kana[0]
		else:
			return "a"

	def get_artist_name(self):
		a = ""
		artists = self.artist.all()
		if artists:
			for artist in artists:
				a = a + artist.__str__() + " "
		return a

	def __str__(self):
		return self.name

class SongNew(models.Model):
	song_name = models.CharField('曲名', max_length=200)
	song_name_kana = models.CharField('曲名カナ', max_length=200, null=True, blank=True)
	artist_name = models.TextField('アーティスト名', max_length=400, null=True, blank=True)
	artist_name_kana = models.TextField('アーティスト名カナ', max_length=400, null=True, blank=True)
	tag = models.TextField('タグ', max_length=400, null=True, blank=True)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='登録者')

	def __str__(self):
		return self.song_name + " - " + self.artist_name

	def artist_name_all(self):
		return self.artist_name.split('\n')

	def tag_all(self):
		return self.tag.split('\n')

class VocalNew(models.Model):
	name = models.CharField('ボーカル名', max_length=200)
	name_kana = models.CharField('ボーカル名カナ', max_length=200, null=True, blank=True)
	class Meta:
		ordering = ('name_kana', 'name')

	def initial(self):
		if self.name_kana:
			return self.name_kana[0]
		else:
			return "a"

	def __str__(self):
		return self.name