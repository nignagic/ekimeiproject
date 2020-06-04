from django import template
from moviedatabase.models import StationService, LineService
register = template.Library()

@register.filter(name='get_station_service')
def get_station_service(value):
	return StationService.objects.get(pk=value)

@register.filter(name='get_line_service')
def get_line_service(value):
	s = StationService.objects.get(pk=value)
	return LineService.objects.get(pk=s.line_service.pk)