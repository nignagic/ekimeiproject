from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Creator)
admin.site.register(Name)
admin.site.register(YoutubeChannel)
admin.site.register(NiconicoAccount)
admin.site.register(TwitterAccount)
admin.site.register(PageLink)
admin.site.register(MovieCategory)
admin.site.register(Movie)
admin.site.register(Part)
admin.site.register(StationInMovie)
admin.site.register(LineInMovie)
admin.site.register(MovieUpdateInformation)
admin.site.register(NoticeInformation)
admin.site.register(UpdateHistory)
admin.site.register(AccountAndCreatorApplication)
admin.site.register(TopImage)