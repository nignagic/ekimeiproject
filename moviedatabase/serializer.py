from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from .models import *

class StationServiceSerializer(serializers.ModelSerializer):
	company_short_name = serializers.CharField(source='line_service.company.short_name_2')
	line_service_pk = serializers.IntegerField(source='line_service.id')
	line_service_name = serializers.CharField(source='line_service.__str__')
	line_service_f_or_s = serializers.CharField(source='line_service.f_or_s')
	line_name = serializers.CharField(source='station.line.with_sub')
	station_service_pk = serializers.IntegerField(source='id')

	get_group_station = serializers.IntegerField(source='station.get_group_station_id')
	pref = serializers.CharField(source='get_pref')
	category = serializers.CharField(source='line_service.category.icon')
	other_option = serializers.BooleanField(source='line_service.company.other_option')
	class Meta:
		model = StationService
		fields = ('name', '__str__', 'station_service_pk', 'company_short_name', 'line_service_pk', 'line_service_name', 'line_service_f_or_s', 'line_name', 'get_group_station', 'get_color', 'status_text', 'pref', 'get_color', 'is_representative', 'category', 'other_option')

class StationSerializer(serializers.ModelSerializer):
	line_pk = serializers.IntegerField(source='line.id')
	station_pk = serializers.IntegerField(source='id')
	lines = serializers.CharField(source='get_group_station_lines')
	class Meta:
		model = Station
		fields = ['__str__', 'station_pk', 'line_pk', 'lines', 'name']

class LineServiceSerializer(serializers.ModelSerializer):
	line_service_pk = serializers.IntegerField(source='id')
	company_short_name = serializers.CharField(source='company.short_name_2')
	class Meta:
		model = LineService
		fields = ('__str__', 'line_service_pk', 'company_short_name', 'name', 'name_sub', 'status_text', 'f_or_s')

class StationInMovieSerializer(serializers.ModelSerializer):
	station_service_pk = serializers.IntegerField(source='station_service.id')
	station_service_name = serializers.CharField(source='station_service.name')
	get_group_station = serializers.IntegerField(source='station_service.station.get_group_station_id')
	line_service_pk = serializers.IntegerField(source='station_service.line_service.pk')
	line_service_name = serializers.CharField(source='station_service.line_service')
	pref = serializers.CharField(source='station_service.get_pref')
	get_color = serializers.CharField(source='station_service.get_color')
	is_representative = serializers.BooleanField(source='station_service.is_representative')
	category = serializers.CharField(source='station_service.line_service.category.icon')
	other_option = serializers.BooleanField(source='station_service.line_service.company.other_option')
	class Meta:
		model = StationInMovie
		fields = ['station_service_name', 'sung_name', 'explanation', 'station_service_pk', 'get_group_station', 'line_service_pk', 'line_service_name', 'pref', 'get_color', 'back_rel', 'is_representative', 'category', 'other_option', 'line_service_on_other_options', 'line_name_customize']

class MovieSerializer(serializers.ModelSerializer):
	movie_pk = serializers.IntegerField(source='id')
	movie_name = serializers.CharField(source='title')
	channel_name = serializers.CharField(source='channel.name')
	class Meta:
		model = LineService
		fields = ('movie_pk', 'movie_name', 'channel_name')
		
class NameSerializer(serializers.ModelSerializer):
	name_pk = serializers.IntegerField(source='id')
	name = serializers.CharField(source='__str__')
	creator_name = serializers.CharField(source='creator.name')
	class Meta:
		model = LineService
		fields = ('name_pk', 'name', 'creator_name')
		
class MovieIsExistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = ['main_id']