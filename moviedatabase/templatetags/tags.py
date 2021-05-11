from django import template
from moviedatabase.models import StationService, LineService, Station, Line
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

@register.filter(name='get_group_station')
def get_group_station(value):
	if value:
		return Station.objects.get(pk=value).group_station_new
	else:
		return "デフォルト（DB新規駅）"

@register.filter(name='get_group_station_line')
def get_group_station_line(value):
	if value:
		station = Station.objects.get(pk=value)
		ss = Station.objects.filter(group_station_new=station.group_station_new)
		l = Line.objects.none()
		for s in ss:
			l |= Line.objects.filter(pk=s.line.id)
		return l
	else:
		return ""