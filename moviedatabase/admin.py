from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Creator)
admin.site.register(Name)
admin.site.register(YoutubeChannel)
admin.site.register(MovieCategory)
admin.site.register(Movie)
admin.site.register(Part)
admin.site.register(StationInMovie)
admin.site.register(LineInMovie)
admin.site.register(MovieUpdateInformation)