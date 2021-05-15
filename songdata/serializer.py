from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from .models import *

class SongSerializer(serializers.ModelSerializer):
	song_pk = serializers.IntegerField(source='id')
	song_initial = serializers.CharField(source='initial')
	song_name = serializers.CharField(source='name')
	artist_name = serializers.CharField(source='get_artist_name')
	class Meta:
		model = Song
		fields = ('__str__', 'song_pk', 'song_initial', 'song_name', 'artist_name')

class VocalNewSerializer(serializers.ModelSerializer):
	vocal_pk = serializers.IntegerField(source='id')
	vocal_name = serializers.CharField(source='name')
	class Meta:
		model = VocalNew
		fields = ('vocal_pk', 'vocal_name')