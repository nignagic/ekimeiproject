from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'songdata'

urlpatterns = [
	path('popup/song_create/', views.PopupSongCreate.as_view(), name='popup_song_create'),
	path('popup/artist_create/', views.PopupArtistCreate.as_view(), name='popup_artist_create'),
	path('popup/vocal_create', views.PopupVocalCreate.as_view(), name='popup_vocal_create'),
]