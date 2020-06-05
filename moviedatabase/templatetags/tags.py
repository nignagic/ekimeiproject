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

@register.simple_tag
def url_replace(request, field, value):
	"""GETパラメータを一部置き換える"""

	url_dict = request.GET.copy()
	url_dict[field] = str(value)
	return url_dict.urlencode()