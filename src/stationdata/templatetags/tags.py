from django import template
from moviedatabase.models import Station, Line
register = template.Library()

@register.filter(name='get_group_station')
def get_group_station(value):
	return Station.objects.get(pk=value)