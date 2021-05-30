from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'moviedatabase'

urlpatterns = [
	path('', views.Top.as_view(), name='top'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.Logout.as_view(), name='logout'),
	path('mypage/', views.Mypage, name='mypage'),
	path('terms/', views.Terms, name='terms'),
	path('privacy/', views.Privacy, name='privacy'),
	path('test/', views.test, name='test'),

	path('search/', views.FreeSearchView, name='freesearch'),

	path('railway/', views.RailwayTopView.as_view(), name='railwaytop'),
	path('railway/belongs_category/<int:category>/', views.MovieListbyBelongsCategoryView.as_view(), name='movielistbybelongscategory'),
	path('railway/movie_category/<int:category>/', views.MovieListbyMovieCategoryView.as_view(), name='movielistbymoviecategory'),
	path('railway/region/<int:region>/', views.CompanyListbyRegionView.as_view(), name='companylistbyregion'),
	path('railway/pref/<int:pref>/line/', views.LineServiceListbyPrefectureView.as_view(), name='lineservicelistbyprefecture'),
	path('railway/company/<int:company>/line/', views.LineServiceListbyCompanyView.as_view(), name='lineservicelistbycompany'),
	path('railway/company/<int:company>/pref/<int:pref>/line/', views.LineServiceListbyCompanyandPrefectureView.as_view(), name='lineservicelistbycompanyandprefecture'),
	path('railway/search/line/', views.LineServiceSearchView.as_view(), name='lineservicesearch'),
	path('railway/search/station/', views.StationServiceSearchView.as_view(), name='stationservicesearch'),

	path('railway/line/formal/<int:line>/', views.MovieListbyLineView.as_view(), name='movielistbyline'),
	path('railway/station/formal/<int:station>/', views.MovieListbyStationView.as_view(), name='movielistbystation'),
	path('railway/line/<int:line_service>/', views.MovieListbyLineServiceView.as_view(), name='movielistbylineservice'),
	path('railway/station/<int:station_service>/', views.MovieListbyStationServiceView.as_view(), name='movielistbystationservice'),
	path('railway/search/sung_name/', views.MovieListbyStationInMovieSearchView.as_view(), name='movielistbystationinmoviesearch'),

	path('music/', views.MusicTopView.as_view(), name='musictop'),
	path('music/search/artist/', views.ArtistSearchView.as_view(), name='artistsearch'),
	path('music/search/song/', views.SongSearchView.as_view(), name='songsearch'),
	path('music/search/songtag/', views.SongTagSearchView.as_view(), name='songtagsearch'),

	path('creator/', views.CreatorTopView.as_view(), name='creatortop'),

	path('creator/movie/<int:creator>/', views.MovieListbyCreatorView.as_view(), name='movielistbycreator'),
	path('creator/channel/<slug:channel_id>/', views.MovieListbyChannelView.as_view(), name='movielistbychannel'),
	path('creator/niconico/<slug:niconico_account>/', views.MovieListbyNiconicoView.as_view(), name='movielistbyniconico'),
	path('creator/search/', views.CreatorSearchView.as_view(), name='creatorsearch'),

	path('movie/', views.MovieListView.as_view(), name='movielist'),
	path('movie/detail/<slug:main_id>/', views.detail_movie, name='detail'),

	path('movie/register/', views.MovieRegisterView.as_view(), name='register'),
	path('movie/edit/<slug:main_id>/', views.movie_edit, name='movie_edit'),
	path('movie/edit/<slug:main_id>/part/', views.movie_part_edit, name='part_edit'),
	path('movie/edit/<slug:main_id>/part/<int:sort_by_movie>', views.movie_part_station_edit, name='station_edit'),
	path('movie/edit/<slug:main_id>/confirm', views.confirm_movie, name='confirm'),
	path('popup/name_create/', views.PopupNameCreate.as_view(), name='popup_name_create'),
	path('popup/parent_movie_setting/', views.popup_parent_movie_setting, name='popup_parent_movie_setting'),
	path('popup/related_movie_setting/', views.popup_related_movie_setting, name='popup_related_movie_setting'),
	path('popup/participant_setting/', views.popup_participant_setting, name='popup_participant_setting'),

	path('updateinformation/<slug:main_id>/', views.UpdateInformation, name='updateinformation'),
	path('updateinformationforuser/<int:creator>/', views.UpdateInformationforCreator, name='updateinformationforcreator'),

	path('application/account_and_creator/', views.AccountAndCreatorApplicationView, name='accountandcreatorapplication'),
	path('application/account_and_creator/confirm/<int:creator>/', views.AccountAndCreatorApplicationConfirmView, name='accountandcreatorapplicationconfirm'),

	url('^api/lineservice/(?P<line_service>.+)/stationservice/', views.StationServicebyLineServiceViewSet.as_view(), name='stationservicebylineserviceapi'),
	url('^api/pref/(?P<pref>.+)/lineservice/', views.LineServicebyPrefectureViewSet.as_view(), name='lineservicebyprefectureapi'),
	url('^api/company/(?P<company>.+)/lineservice/', views.LineServicebyCompanyViewSet.as_view(), name='lineservicebycompanyapi'),
	url('^api/line/(?P<line>.+)/station', views.StationbyLineViewSet.as_view(), name='stationbylineapi'),
	url('^api/stationsearch/(?P<word>.+)/$', views.StationServiceSearchViewSet.as_view(), name='stationservicesearchapi'),
	url('^api/groupstationsearch/(?P<word>.+)/$', views.GroupStationSearchViewSet.as_view(), name='groupstationsearchapi'),
	url('^api/transfer/(?P<station_service>.+)/$', views.LineServiceTransferViewSet.as_view(), name='lineservicetransferapi'),
	url('^api/partstation/(?P<id>.+)/$', views.PartStationViewSet.as_view(), name='partstationapi'),
	url('^api/channel/(?P<channel>.+)/movie/', views.MoviebyChannelViewSet.as_view(), name='moviebychannelapi'),
	url('^api/movie/(?P<movie>.+)/', views.MovieViewSet.as_view(), name='movieapi'),
	url('^api/creator/(?P<creator>.+)/name/', views.NamebyCreatorViewSet.as_view(), name='namebycreatorapi'),
	url('^api/name/(?P<name>.+)/', views.NameViewSet.as_view(), name='nameapi'),
]