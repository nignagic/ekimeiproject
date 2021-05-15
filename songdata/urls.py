from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'songdata'

urlpatterns = [
	path('popup/song_create/', views.PopupSongCreate.as_view(), name='popup_song_create'),
	path('popup/artist_create/', views.PopupArtistCreate.as_view(), name='popup_artist_create'),
	path('popup/vocal_create', views.PopupVocalCreate.as_view(), name='popup_vocal_create'),
	path('popup/song_setting', views.popup_song_setting, name='popup_song_setting'),
	path('popup/vocal_setting', views.popup_vocal_setting, name='popup_vocal_setting'),
	url('^api/artist/(?P<artist>.+)/song', views.SongbyArtistViewSet.as_view(), name='songbyartistapi'),
	url('^api/song/(?P<song>.+)', views.SongViewSet.as_view(), name='songapi'),
	url('^api/vocal/(?P<vocal>.+)', views.VocalViewSet.as_view(), name='vocalapi'),
]