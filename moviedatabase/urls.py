from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'moviedatabase'

urlpatterns = [
	path('', views.Top.as_view(), name='top'),
	path('notice/', views.NoticeList.as_view(), name='noticelist'),
	path('notice/<int:pk>', views.NoticeDetail.as_view(), name='notice'),
	path('update/', views.UpdateList.as_view(), name='updatelist'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.Logout.as_view(), name='logout'),
	path('mypage/', views.Mypage, name='mypage'),
	path('terms/', views.Terms, name='terms'),
	path('privacy/', views.Privacy, name='privacy'),
	path('guide_account_creator/', views.GuideAccountCreator, name='guideaccountcreator'),
	path('startup_guide/', views.StartUpGuide, name='startupguide'),
	path('line_customize_guide/', views.LineCustomizeGuide, name='linecustomizeguide'),

	path('test/', views.test, name='test'),
	# path('mail/', views.mail, name='mail'),
	# path('send_twitter', views.send_twitter, name="send_twitter"),
	# path('twitter', views.tweet, name="twitter"),
	# path('callback', views.callback, name="callback"),

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
	# path('music/search/artist/', views.ArtistSearchView.as_view(), name='artistsearch'),
	# path('music/search/song/', views.SongSearchView.as_view(), name='songsearch'),
	# path('music/search/songtag/', views.SongTagSearchView.as_view(), name='songtagsearch'),
	# path('music/vocal/<int:vocal>', views.MovieListbyVocalView.as_view(), name='songtagsearch'),

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
	path('movie/edit/station/multiple/upload', views.MultipleStationUpload, name='multiplestationupload'),
	path('movie/edit/station/multiple/search', views.MultipleStationSearch, name='multiplestationsearch'),
	path('popup/name_create/', views.PopupNameCreate.as_view(), name='popup_name_create'),
	path('popup/parent_movie_setting/', views.popup_parent_movie_setting, name='popup_parent_movie_setting'),
	path('popup/related_movie_setting/', views.popup_related_movie_setting, name='popup_related_movie_setting'),
	path('popup/participant_setting/', views.popup_participant_setting, name='popup_participant_setting'),

	path('movie/edit/<slug:main_id>/statistics/update', views.movie_statistics_update, name='movie_statistics_update'),

	path('updateinformationforuser/<int:creator>/', views.UpdateInformationforCreator, name='updateinformationforcreator'),

	path('application/account_and_creator/', views.AccountAndCreatorApplicationView, name='accountandcreatorapplication'),
	path('application/account_and_creator/confirm/<int:creator>/', views.AccountAndCreatorApplicationConfirmView, name='accountandcreatorapplicationconfirm'),

	path('check/channel_movie_is_exist/<slug:channel_id>/', views.ChannelMovieIsExist, name='channel_movie_is_exist'),

	path('api/lineservice/<line_service>/stationservice/', views.StationServicebyLineServiceViewSet.as_view(), name='stationservicebylineserviceapi'),
	path('api/pref/<pref>/lineservice/', views.LineServicebyPrefectureViewSet.as_view(), name='lineservicebyprefectureapi'),
	path('api/company/<company>/lineservice/', views.LineServicebyCompanyViewSet.as_view(), name='lineservicebycompanyapi'),
	path('api/line/<line>/station', views.StationbyLineViewSet.as_view(), name='stationbylineapi'),
	path('api/stationsearch/<station>/', views.StationServiceSearchViewSet.as_view(), name='stationservicesearchapi'),
	path('api/stationwithlinesearch/<station>/<line>/', views.StationServiceWithLineSearchViewSet.as_view(), name='stationservicewithlinesearchapi'),
	path('api/groupstationsearch/<word>/', views.GroupStationSearchViewSet.as_view(), name='groupstationsearchapi'),
	path('api/transfer/<station_service>/', views.LineServiceTransferViewSet.as_view(), name='lineservicetransferapi'),
	path('api/partstation/<id>/', views.PartStationViewSet.as_view(), name='partstationapi'),
	path('api/channel/<channel>/movie/', views.MoviebyChannelViewSet.as_view(), name='moviebychannelapi'),
	path('api/movie/<movie>/', views.MovieViewSet.as_view(), name='movieapi'),
	path('api/creator/<creator>/name/', views.NamebyCreatorViewSet.as_view(), name='namebycreatorapi'),
	path('api/name/<name>/', views.NameViewSet.as_view(), name='nameapi'),
	path('api/movie_is_exist/<main_id>/', views.MovieIsExistViewSet.as_view(), name='movieisexistapi'),
]