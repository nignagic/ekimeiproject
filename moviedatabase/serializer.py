from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from .models import *

class StationServiceSerializer(serializers.ModelSerializer):
	line_service_pk = serializers.IntegerField(source='line_service.id')
	line_service_name = serializers.CharField(source='line_service.name')
	station_service_pk = serializers.IntegerField(source='id')
	class Meta:
		model = StationService
		fields = ('__str__', 'station_service_pk', 'line_service_pk', 'line_service_name', 'get_color')

class StationSerializer(serializers.ModelSerializer):
	line_pk = serializers.IntegerField(source='line.id')
	station_pk = serializers.IntegerField(source='id')
	class Meta:
		model = StationService
		fields = ('__str__', 'station_pk', 'line_pk', 'name')

class LineServiceSerializer(serializers.ModelSerializer):
	line_service_pk = serializers.IntegerField(source='id')
	class Meta:
		model = LineService
		fields = ('__str__', 'line_service_pk')

class StationInMovieSerializer(serializers.ModelSerializer):
	station_service_pk = serializers.IntegerField(source='station_service.id')
	get_group_station = serializers.IntegerField(source='station_service.station.get_group_station_id')
	line_service_pk = serializers.IntegerField(source='station_service.line_service.pk')
	line_service_name = serializers.CharField(source='station_service.line_service')
	pref = serializers.CharField(source='station_service.get_pref')
	get_color = serializers.CharField(source='station_service.get_color')
	is_representative = serializers.BooleanField(source='station_service.is_representative')
	category = serializers.CharField(source='station_service.line_service.category.icon')
	class Meta:
		model = StationInMovie
		fields = ['sung_name', 'station_service_pk', 'get_group_station', 'line_service_pk', 'line_service_name', 'pref', 'get_color', 'back_rel', 'is_representative', 'category']