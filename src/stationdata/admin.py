from django.contrib import admin
from .models import *

# Register your models here.
class StationAdmin(admin.ModelAdmin):
	list_display = ('name', 'line')
	search_fields = ['name']

class StationServiceAdmin(admin.ModelAdmin):
	list_display = ('name', 'line_service', 'get_color', 'is_representative')
	list_editable = ('is_representative',)
	search_fields = ('name', 'line_service__name')

# class StationInMovieAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'id_in_movie', 'station_cd', 'station_name')
# 	search_fields = ['station_name']

# class MovieAdmin(admin.ModelAdmin):
# 	list_display = ('title', 'channel', 'main_id', 'published_at', 'is_collab')

admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Prefecture)
admin.site.register(CompanyCategory)
admin.site.register(Company)
admin.site.register(BelongsCategory)
admin.site.register(Line)
admin.site.register(Station, StationAdmin)
admin.site.register(LineService)
admin.site.register(StationService, StationServiceAdmin)
admin.site.register(StationServiceHistory)
admin.site.register(ErrorList)