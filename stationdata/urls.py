from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'stationdata'

urlpatterns = [
	path('upload/', views.upload.as_view(), name='upload'),

	path('upload/country/', views.uploadCountry, name='uploadCountry'),
	path('upload/region/', views.uploadRegion, name='uploadRegion'),
	path('upload/prefecture/', views.uploadPrefecture, name='uploadPrefecture'),
	path('upload/companycategory/', views.uploadCompanyCategory, name='uploadCompanyCategory'),
	path('upload/company/', views.uploadCompany, name='uploadCompany'),
	path('upload/line/', views.uploadLine, name='uploadLine'),
	path('upload/station/', views.uploadStation, name='uploadStation'),
	path('upload/lineservice/', views.uploadLineService, name='uploadLineService'),
	path('upload/stationservice/', views.uploadStationService, name='uploadStationService'),

	path('delete/company/', views.CompanyDelete, name='CompanyDelete'),
	path('delete/line/', views.LineDelete, name='LineDelete'),
	path('delete/station/', views.StationDelete, name='StationDelete'),
	path('delete/lineservice', views.LineServiceDelete, name='LineServiceDelete'),
	path('delete/stationservice', views.StationServiceDelete, name='StationServiceDelete'),
	path('delete/errorlist', views.ErrorListDelete, name='ErrorListDelete'),

	path('register/company/', views.CompanyRegisterView.as_view(), name='companyregister'),
	path('register/line/<int:company>', views.LineRegisterView, name='lineregister'),
	path('register/station/<int:line>', views.StationRegisterView, name='stationregister'),
	path('register/lineservice/<int:company>', views.LineServiceRegisterView, name='lineserviceregister'),
	path('register/simple/lineservice/', views.LineServiceSimpleRegisterView.as_view(), name='lineservicesimpleregister'),
	path('register/s/lineservice/', views.PopupLineServiceSimpleRegisterView.as_view(), name='popuplineservicesimpleregister'),
	path('register/s/company/', views.PopupCompanySimpleRegisterView.as_view(), name='popupcompanysimpleregister'),
	path('register/s/category/', views.PopupBelongsCategorySimpleRegisterView.as_view(), name='popupbelongscategorysimpleregister'),
	path('edit/lineservice/<int:company>', views.LineServiceEditbyCompanyView, name='lineserviceeditbycompany'),
	path('register/stationservice/<int:line_service>', views.StationServiceRegisterView, name='stationserviceregister'),

	path('stationkanaset/', views.stationkanaset, name='stationkanaset'),
	path('stationgroupset/', views.stationgroupset, name='stationgroupset'),
	path('stationservicegroupset/', views.stationservicegroupset, name='stationservicegroupset'),
	path('lineprefset/', views.lineprefset, name='lineprefset'),
	path('lineserviceprefset/', views.lineserviceprefset, name='lineserviceprefset'),
	path('lineservicelineset/', views.lineservicelineset, name='lineservicelineset'),
]