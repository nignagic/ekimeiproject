from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'moviedatabase'

urlpatterns = [
	path('', views.Top.as_view(), name='top'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.Logout.as_view(), name='logout'),

	path('railway/', views.RailwayTopView.as_view(), name='railwaytop'),
	path('railway/category/', views.BelongsCategoryListView.as_view(), name='categorylist'),
	path('railway/country/<int:country>/', views.LineServiceListbyCountryView.as_view(), name='lineservicelistbycountry'),
	path('railway/region/<int:region>/category/<slug:category>', views.CompanyListbyRegionView.as_view(), name='companylistbyregion'),
	path('railway/pref/<int:pref>/line/', views.LineServiceListbyPrefectureView.as_view(), name='lineservicelistbyprefecture'),
	path('railway/company/<int:company>/line/', views.LineServiceListbyCompanyView.as_view(), name='lineservicelistbycompany'),
	path('railway/company/<int:company>/pref/<int:pref>/line/', views.LineServiceListbyCompanyandPrefectureView.as_view(), name='lineservicelistbycompanyandprefecture'),
	path('railway/category/<int:category>/line/', views.LineServiceListbyCategoryView.as_view(), name='lineservicelistbycategory'),
	path('railway/category/<int:category>/pref/<int:pref>/line/', views.LineServiceListbyCategoryandPrefectureView.as_view(), name='lineservicelistbycategoryandprefecture'),
	path('railway/search/line/', views.LineServiceSearchView.as_view(), name='lineservicesearch'),
	path('railway/search/station/', views.StationServiceSearchView.as_view(), name='stationservicesearch'),

	path('railway/line/formal/<int:line>/<slug:sort>/<slug:order>/', views.MovieListbyLineView.as_view(), name='movielistbyline'),
	path('railway/station/formal/<int:station>/<slug:sort>/<slug:order>/', views.MovieListbyStationView.as_view(), name='movielistbystation'),
	path('railway/line/<int:line_service>/<slug:sort>/<slug:order>/', views.MovieListbyLineServiceView.as_view(), name='movielistbylineservice'),
	path('railway/station/<int:station_service>/<slug:sort>/<slug:order>/', views.MovieListbyStationServiceView.as_view(), name='movielistbystationservice'),

	path('music/', views.MusicTopView.as_view(), name='musictop'),
	path('music/artist/<slug:kana>/', views.ArtistListView.as_view(), name='artistlist'),
	path('music/song/<slug:kana>/', views.SongListView.as_view(), name='songlist'),
	path('music/artist/<int:artist>/song/<slug:kana>/', views.SongListbyArtistView.as_view(), name='songlistbyartist'),
	# path('music/vocal/<slug:kana>/', views.VocalListView.as_view(), name='vocallist'),
	path('music/search/artist/', views.ArtistSearchView.as_view(), name='artistsearch'),
	path('music/search/song/', views.SongSearchView.as_view(), name='songsearch'),

	path('music/artist/<int:artist>/<slug:sort>/<slug:order>/', views.MovieListbyArtistView.as_view(), name='movielistbyartist'),
	path('music/song/<int:song>/<slug:sort>/<slug:order>/', views.MovieListbySongView.as_view(), name='movielistbysong'),
	# path('music/vocal/<int:vocal>/<slug:sort>/<slug:order>/', views.MovieListbyVocalView.as_view(), name='movielistbyvocal'),

	path('creator/list/<slug:kana>/', views.CreatorListView.as_view(), name='creatortop'),
	# path('creator/channel/', views.ChannelListView.as_view(), name='channellist'),

	path('creator/<int:creator>/<slug:sort>/<slug:order>/', views.MovieListbyCreatorView.as_view(), name='movielistbycreator'),
	# path('creator/name/<int:name>/<slug:sort>/<slug:order>/', views.MovieListbyNameView.as_view(), name='movielistbyname'),
	path('creator/channel/<slug:channel_id>/<slug:sort>/<slug:order>/', views.MovieListbyChannelView.as_view(), name='movielistbychannel'),
	path('creator/niconico/<slug:niconico_account>/<slug:sort>/<slug:order>/', views.MovieListbyNiconicoView.as_view(), name='movielistbyniconico'),
	path('creator/search/', views.CreatorSearchView.as_view(), name='creatorsearch'),

	path('movie/', views.MovieListView.as_view(), name='movielist'),
	path('movie/detail/<slug:main_id>/', views.detail_movie, name='detail'),

	path('movie/register/', views.MovieRegisterView.as_view(), name='register'),
	path('movie/edit/<slug:main_id>/', views.movie_part_edit, name='part_edit'),
	path('movie/edit/<slug:main_id>/part/<int:sort_by_movie>', views.movie_part_station_edit, name='station_edit'),

	path('updateinformation/<slug:main_id>/', views.UpdateInformation, name='updateinformation'),
	path('updateinformationforuser/<int:creator>/', views.UpdateInformationforCreator, name='updateinformationforcreator'),

	url('^api/lineservice/(?P<line_service>.+)/stationservice/', views.StationServicebyLineServiceViewSet.as_view(), name='stationservicebylineserviceapi'),
	url('^api/pref/(?P<pref>.+)/lineservice/', views.LineServicebyPrefectureViewSet.as_view(), name='lineservicebyprefectureapi'),
	url('^api/company/(?P<company>.+)/lineservice/', views.LineServicebyCompanyViewSet.as_view(), name='lineservicebycompanyapi'),
	url('^api/line/(?P<line>.+)/station', views.StationbyLineViewSet.as_view(), name='stationbylineapi'),
	url('^api/stationsearch/(?P<word>.+)/$', views.StationServiceSearchViewSet.as_view(), name='stationservicesearchapi'),
	url('^api/transfer/(?P<station_service>.+)/$', views.LineServiceTransferViewSet.as_view(), name='lineservicetransferapi'),
	url('^api/partstation/(?P<id>.+)/$', views.PartStationViewSet.as_view(), name='partstationapi'),
]