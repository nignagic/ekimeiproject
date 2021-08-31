from django import template
from moviedatabase.models import StationService, LineService, Station, Line, StationInMovie
register = template.Library()

@register.filter(name='get_station_service')
def get_station_service(value):
	if value:
		return StationService.objects.get(pk=value)

@register.filter(name='get_line_service')
def get_line_service(value):
	if value:
		s = StationService.objects.get(pk=value)
		return LineService.objects.get(pk=s.line_service.pk)

@register.simple_tag
def url_replace(request, field, value):
	"""GETパラメータを一部置き換える"""

	url_dict = request.GET.copy()
	url_dict[field] = str(value)
	return url_dict.urlencode()

# station_edit.html用

@register.filter(name='get_group_station_from_service')
def get_group_station_from_service(value):
	if value:
		stationservice = StationService.objects.get(pk=value)
		return Station.objects.get(pk=stationservice.station.pk).get_group_station_id()
	else:
		return "デフォルト（DB新規駅）"

@register.filter(name='line_service_pk')
def line_service_pk(value):
	if value:
		return StationService.objects.get(pk=value).line_service.pk
	else:
		return "デフォルト（DB新規駅）"

@register.filter(name='line_customize_name')
def line_customize_name(value):
	if value:
		return StationInMovie.objects.get(pk=value).sung_name
	else:
		return "デフォルト（DB新規駅）"

@register.filter(name='category')
def category(value):
	if value:
		return StationService.objects.get(pk=value).line_service.category.icon
	else:
		return "デフォルト（DB新規駅）"

@register.filter(name='pref')
def pref(value):
	if value:
		return StationService.objects.get(pk=value).get_pref()
	else:
		return "デフォルト（DB新規駅）"

@register.filter(name='get_color')
def get_color(value):
	if value:
		return StationService.objects.get(pk=value).get_color()
	else:
		return "デフォルト（DB新規駅）"

@register.filter(name='is_representative')
def is_representative(value):
	if value:
		return StationService.objects.get(pk=value).is_representative
	else:
		return "デフォルト（DB新規駅）"

@register.filter(name='other_option')
def other_option(value):
	if value:
		return StationService.objects.get(pk=value).line_service.company.other_option
	else:
		return "デフォルト（DB新規駅）"


# station_edit.html用ここまで

@register.filter(name='get_group_station')
def get_group_station(value):
	if value:
		return Station.objects.get(pk=value).group_station_id
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