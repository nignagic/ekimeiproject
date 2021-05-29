from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.urls import reverse_lazy

from .models import *
from . import forms

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
import csv
from io import TextIOWrapper

# Create your views here.
class upload(PermissionRequiredMixin, generic.TemplateView):
	permission_required = ('stationdata.add_station')
	template_name = 'stationdata/upload.html'

@permission_required('stationdata.add_country')
def uploadCountry(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue
			if i == 0:
				i += 1
				continue
			name = line[0]

			item = Country(name=name)
			items.append(item)
		Country.objects.bulk_create(items)

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.add_region')
def uploadRegion(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue
			name = line[0]

			tmp = Country.objects.filter(name__iexact=line[1])
			if tmp.count() == 1:
				country = tmp.first()
			else:
				country = None
				category = 'Region-Country'
				text = line[0] + "'s " + line[1] + " failure."
				ErrorList.objects.create(category=category, text=text)

			item = Region(name=name, country=country)
			items.append(item)
		Region.objects.bulk_create(items)

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.add_prefecture')
def uploadPrefecture(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue
			name = line[0]

			tmp = Region.objects.filter(name__iexact=line[1])
			if tmp.count() == 1:
				region = tmp.first()
			else:
				region = None
				category = 'Prefecture-Region'
				text = line[0] + "'s " + line[1] + " failure."
				ErrorList.objects.create(category=category, text=text)

			item = Prefecture(name=name, region=region)
			items.append(item)
		Prefecture.objects.bulk_create(items)

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.add_companycategory')
def uploadCompanyCategory(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue
			name = line[0]

			item = CompanyCategory(name=name)
			items.append(item)
		CompanyCategory.objects.bulk_create(items)

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.add_company')
def uploadCompany(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue
			name = line[0]
			short_name = line[1]
			short_name_2 = line[2]
			name_kana = line[3]
			color = line[4]

			tmp = CompanyCategory.objects.filter(name__iexact=line[5])
			if tmp.count() == 1:
				category = tmp.first()
			else:
				category = None
				fail_category = 'Company-CompanyCategory'
				text = line[0] + "'s " + line[5] + " failure."
				ErrorList.objects.create(category=fail_category, text=text)			

			sort_by_category = line[6]

			item = Company(
				name=name,
				short_name=short_name,
				short_name_2=short_name_2,
				name_kana=name_kana,
				color=color,
				category=category,
				sort_by_category=sort_by_category)
			items.append(item)
		Company.objects.bulk_create(items)

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.add_line')
def uploadLine(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue
			tmp = BelongsCategory.objects.filter(name__iexact=line[0])
			if tmp.count() == 1:
				category = tmp.first()
			else:
				category = None
				fail_category = 'Line-Category'
				text = line[2] + "'s " + line[0] + " failure."
				ErrorList.objects.create(category=fail_category, text=text)			

			formal_name = line[1]
			name = line[2]
			name_sub = line[3]

			tmp = Company.objects.filter(name__iexact=line[4])
			if tmp.count() == 1:
				company = tmp.first()
			else:
				company = None
				fail_category = 'Line-Company'
				text = line[2] + "'s " + line[4] + " failure."
				ErrorList.objects.create(category=fail_category, text=text)			

			sort_by_company = line[5]
			is_freight = line[6]
			status = line[7]

			item = Line(
				category=category,
				formal_name=formal_name,
				name=name,
				name_sub=name_sub,
				company=company,
				sort_by_company=sort_by_company,
				is_freight=is_freight,
				status=status)
			items.append(item)
		Line.objects.bulk_create(items)

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.add_station')
def uploadStation(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue

			name = line[4]

			tmp = Line.objects.filter(company__name__iexact=line[5]).filter(name__iexact=line[6]).filter(name_sub__iexact=line[7])
			if tmp.count() == 1:
				line_line = tmp.first()
			else:
				line_line = None
				fail_category = 'Station-Line'
				text = line[4] + "'s " + line[5] + "-" + line[6] + "-" + line[7] + " failure."
				ErrorList.objects.create(category=fail_category, text=text)			

			sort_by_line = line[8]
			name_kana = line[9]

			tmp = Prefecture.objects.filter(name__iexact=line[10])
			if tmp.count() == 1:
				pref = tmp.first()
			else:
				pref = None
				fail_category = 'Station-Prefecture'
				text = line[4] + "'s " + line[10] + " failure."
				ErrorList.objects.create(category=fail_category, text=text)			

			if line[11] == "":
				open_ymd = None
			else:
				open_ymd = line[11]
			if line[12] == "":
				close_ymd = None
			else:
				close_ymd = line[12]
			lon = line[13]
			lat = line[14]
			status = line[15]

			item = Station(
				name=name,
				line=line_line,
				sort_by_line=sort_by_line,
				name_kana=name_kana,
				pref=pref,
				open_ymd=open_ymd,
				close_ymd=close_ymd,
				lon=lon,
				lat=lat,
				status=status)
			items.append(item)
		Station.objects.bulk_create(items)

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.add_lineservice')
def uploadLineService(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue
			tmp = BelongsCategory.objects.filter(name__iexact=line[0])
			if tmp.count() == 1:
				category = tmp.first()
			else:
				category = None
				fail_category = 'LineService-Category'
				text = line[1] + "'s " + line[0] + " failure."
				ErrorList.objects.create(category=fail_category, text=text)			

			name = line[1]
			name_sub = line[2]
			head_company_name = line[4]

			tmp = Company.objects.filter(name__iexact=line[5])
			if tmp.count() == 1:
				company = tmp.first()
			else:
				company = None
				fail_category = 'LineService-Company'
				text = line[1] + "'s " + line[4] + " failure."
				ErrorList.objects.create(category=fail_category, text=text)			

			sort_by_company = line[6]
			is_formal = line[7]
			is_service = line[8]
			color = line[9]
			status = line[10]

			item = LineService(
				category=category,
				name=name,
				name_sub=name_sub,
				head_company_name=head_company_name,
				company=company,
				sort_by_company=sort_by_company,
				is_formal=is_formal,
				is_service=is_service,
				color=color,
				status=status)
			items.append(item)
		LineService.objects.bulk_create(items)

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.add_stationservice')
def uploadStationService(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue

			name = line[7]

			tmp = Station.objects.filter(name__iexact=line[8]).filter(line__company__name__iexact=line[9]).filter(line__name__iexact=line[10]).filter(line__name_sub__iexact=line[11])
			if tmp.count() == 1:
				station = tmp.first()
			else:
				station = None
				fail_category = 'StationService-Station'
				text = line[7] + "'s " + line[8] + line[9] + line[10] + line[11] + " failure."
				ErrorList.objects.create(category=fail_category, text=text)			

			tmp = LineService.objects.filter(company__name__iexact=line[12]).filter(name__iexact=line[13]).filter(name_sub__iexact=line[14]).filter(is_formal=line[15]).filter(is_service=line[16])
			if tmp.count() == 1:
				line_service = tmp.first()
			else:
				line_service = None
				fail_category = 'StationService-LineService'
				text = line[7] + "'s " + line[12] + line[13] + line[14] + line[15] + line[16] + " failure."
				ErrorList.objects.create(category=fail_category, text=text)			

			numbering_head = line[17]
			numbering_symbol = line[18]
			numbering_middle = line[19]
			numbering_number = line[20]
			sort_by_line_service = line[21]
			color = line[22]

			item = StationService(
				name=name,
				station=station,
				line_service=line_service,
				numbering_head=numbering_head,
				numbering_symbol=numbering_symbol,
				numbering_middle=numbering_middle,
				numbering_number=numbering_number,
				sort_by_line_service=sort_by_line_service,
				color=color)
			items.append(item)
		StationService.objects.bulk_create(items)

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.change_station')
def stationkanaset(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue
			tmp = Station.objects.filter(name__iexact=line[4]).filter(line__company__name__iexact=line[5]).filter(line__name__iexact=line[6]).filter(line__name_sub__iexact=line[7])
			if tmp.count() == 1:
				item = tmp.first()
			else:
				item = None
				fail_category = 'Station-get'
				text = line[4] + "'s " + " station get " + " failure."
				ErrorList.objects.create(category=fail_category, text=text)
				continue

			if line[9]:
				item.name_kana = line[9]
			else:
				item.name_kana = ""

			items.append(item)
		Station.objects.bulk_update(items, fields=[
			'name_kana'
		])

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.change_station')
def stationgroupset(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue
			tmp = Station.objects.filter(name__iexact=line[4]).filter(line__company__name__iexact=line[5]).filter(line__name__iexact=line[6]).filter(line__name_sub__iexact=line[7])
			if tmp.count() == 1:
				item = tmp.first()
			else:
				item = None
				fail_category = 'Station-get'
				text = line[4] + "'s " + " station get " + " failure."
				ErrorList.objects.create(category=fail_category, text=text)
				continue

			if line[0]:
				tmp = Station.objects.filter(name__iexact=line[0]).filter(line__company__name__iexact=line[1]).filter(line__name__iexact=line[2]).filter(line__name_sub__iexact=line[3])
				if tmp.count() == 1:
					item.group_station_new = tmp.first()
				else:
					item.group_station_new = item
					fail_category = 'Station-get'
					text = line[4] + "'s " + " group station " + " failure."
					ErrorList.objects.create(category=fail_category, text=text)
			else:
				item.group_station_new = item

			items.append(item)
		Station.objects.bulk_update(items, fields=[
			'group_station_new'
		])

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')

@permission_required('stationdata.change_stationservice')
def stationservicegroupset(request):
	if 'csv' in request.FILES:
		items = []
		form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
		csv_file = csv.reader(form_data)
		i = 0
		for line in csv_file:
			if i == 0:
				i += 1
				continue
			tmp = StationService.objects.filter(name__iexact=line[7]).filter(station__name__iexact=line[8]).filter(station__line__company__name__iexact=line[9]).filter(station__line__name__iexact=line[10]).filter(station__line__name_sub__iexact=line[11]).filter(line_service__company__name__iexact=line[12]).filter(line_service__name__iexact=line[13]).filter(line_service__name_sub__iexact=line[14]).filter(line_service__is_formal__iexact=line[15]).filter(line_service__is_service__iexact=line[16]).filter(sort_by_line_service__iexact=line[21])
			if tmp.count() == 1:
				item = tmp.first()
			else:
				item = None
				fail_category = 'StationService-get'
				text = line[8] + line[9] + line[10] + line[11] + line[7] + "'s " + " stationservice get " + " failure."
				ErrorList.objects.create(category=fail_category, text=text)
				continue

			if line[0]:
				tmp = StationService.objects.filter(name__iexact=line[0]).filter(line_service__company__name__iexact=line[1]).filter(line_service__name__iexact=line[2]).filter(line_service__name_sub__iexact=line[3]).filter(line_service__is_formal__iexact=line[4]).filter(line_service__is_service__iexact=line[5]).filter(sort_by_line_service__iexact=line[6])
				if tmp.count() == 1:
					item.group_station_service = tmp.first()
				else:
					item.group_station_service = item
					fail_category = 'StationService-get'
					text = line[8] + line[9] + line[10] + line[11] + line[7]  + "'s " + " group stationservice " + " failure."
					ErrorList.objects.create(category=fail_category, text=text)
			else:
				item.group_station_service = item

			items.append(item)
		StationService.objects.bulk_update(items, fields=[
			'group_station_service'
		])

		return render(request, 'stationdata/upload.html')

	else:
		return render(request, 'stationdata/upload.html')


@permission_required('stationdata.delete_company')
def CompanyDelete(request):
	Company.objects.all().delete()
	return render(request, 'stationdata/upload.html')

@permission_required('stationdata.delete_line')
def LineDelete(request):
	Line.objects.all().delete()
	return render(request, 'stationdata/upload.html')

@permission_required('stationdata.delete_station')
def StationDelete(request):
	Station.objects.all().delete()
	return render(request, 'stationdata/upload.html')

@permission_required('stationdata.delete_lineservice')
def LineServiceDelete(request):
	LineService.objects.all().delete()
	return render(request, 'stationdata/upload.html')

@permission_required('stationdata.delete_stationservice')
def StationServiceDelete(request):
	StationService.objects.all().delete()
	return render(request, 'stationdata/upload.html')

@permission_required('stationdata.delete_errorlist')
def ErrorListDelete(request):
	ErrorList.objects.all().delete()
	return render(request, 'stationdata/upload.html')

class CompanyRegisterView(PermissionRequiredMixin, generic.CreateView):
	template_name = 'stationdata/companyregister.html'
	model = Company
	form_class = forms.CompanyRegisterForm
	permission_required = ("stationdata.add_company",)
	def get_success_url(self):
		return reverse_lazy('stationdata:lineregister', kwargs={'company': self.object.pk})

@permission_required('stationdata.add_line')
# def LineRegisterView(request, company):
# 	company = get_object_or_404(Company, pk=company)
# 	form = forms.LineRegisterForm(request.POST or None)
# 	if request.method == 'POST' and form.is_valid():
# 		form.save()
# 		line = Line.objects.latest('pk')
# 		lineservice, created = LineService.objects.get_or_create(category=line.category, name=line.name, company=line.company, is_formal=1)
# 		return redirect('stationdata:stationregister', line=line.pk)

# 	context = {
# 		'company': company,
# 		'form': form
# 	}

# 	return render(request, 'stationdata/lineregister.html', context)

@permission_required('stationdata.add_line')
def LineRegisterView(request, company):
	company = get_object_or_404(Company, pk=company)
	formset = forms.LineRegisterFormset(request.POST or None, instance=company)
	if request.method == 'POST' and formset.is_valid():
		formset.save()
		return redirect('moviedatabase:lineservicelistbycompany', company=company.pk)

	prefs = Prefecture.objects.all()
	categories = BelongsCategory.objects.all()

	context = {
		'company': company,
		'formset': formset,
		'prefs': prefs,
		'categories': categories
	}

	return render(request, 'stationdata/lineregister.html', context)

@permission_required('stationdata.add_station')
def StationRegisterView(request, line):
	line = get_object_or_404(Line, pk=line)
	formset = forms.StationRegisterFormset(request.POST or None, instance=line)
	if request.method == 'POST' and formset.is_valid():
		formset.save()
		stations = Station.objects.filter(line=line)
		prefs = Prefecture.objects.none()
		for station in stations:
			if station.group_station_new == None:
				station.group_station_new = station
				station.save()
			if station.pref:
				prefs |= Prefecture.objects.filter(pk=station.pref.pk)
		for pref in prefs:
			line.prefs.add(pref)
		return redirect('moviedatabase:movielistbyline', line=line.pk)

	prefs = Prefecture.objects.all()

	context = {
		'line': line,
		'formset': formset,
		'prefs': prefs
	}

	return render(request, 'stationdata/stationregister.html', context)

class LineServiceSimpleRegisterView(PermissionRequiredMixin, generic.CreateView):
	model = LineService
	fields = ('category', 'name', 'name_sub', 'company', 'color', 'prefs')
	permission_required = ('stationdata.add_lineservice')
	success_url = reverse_lazy('moviedatabase:railwaytop')

class PopupLineServiceSimpleRegisterView(LineServiceSimpleRegisterView):
	def form_valid(self, form):
		lineservice = form.save()

		line, created = Line.objects.get_or_create(category=lineservice.category, name=lineservice.name, name_sub=lineservice.name_sub, company=lineservice.company)
		representativename = line.name + "(代表オブジェクト)"
		if lineservice.prefs.all():
			for p in lineservice.prefs.all():
				station, created = Station.objects.get_or_create(name=representativename, line=line, pref=p, is_representative=True)
				stationservice, created = StationService.objects.get_or_create(name=representativename, station=station, line_service=lineservice, color=lineservice.color, is_representative=True)
				line.prefs.add(p)
		else:
			station, created = Station.objects.get_or_create(name=representativename, line=line, is_representative=True)
			stationservice, created = StationService.objects.get_or_create(name=representativename, station=station, line_service=lineservice, color=lineservice.color, is_representative=True)

		context = {
			'object_name': str(lineservice),
			'object_pk': lineservice.pk,
			'function_name': 'add_lineservice'
		}
		return render(self.request, 'stationdata/close.html', context)

class CompanySimpleRegisterView(PermissionRequiredMixin, generic.CreateView):
	model = Company
	fields = ('name', 'short_name', 'short_name_2', 'name_kana', 'color')
	permission_required = ('stationdata.add_company')
	success_url = reverse_lazy('moviedatabase:railwaytop')

class PopupCompanySimpleRegisterView(CompanySimpleRegisterView):
	def form_valid(self, form):
		company = form.save()
		context = {
			'object_name': str(company),
			'object_pk': company.pk,
			'function_name': 'add_company'
		}
		return render(self.request, 'stationdata/close.html', context)

class BelongsCategorySimpleRegisterView(PermissionRequiredMixin, generic.CreateView):
	model = BelongsCategory
	fields = ('name',)
	permission_required = ('stationdata.add_belongscategory')
	success_url = reverse_lazy('moviedatabase:railwaytop')

class PopupBelongsCategorySimpleRegisterView(BelongsCategorySimpleRegisterView):
	def form_valid(self, form):
		belongscategory = form.save()
		context = {
			'object_name': str(belongscategory),
			'object_pk': belongscategory.pk,
			'function_name': 'add_belongscategory'
		}
		return render(self.request, 'stationdata/close.html', context)

@permission_required('moviedatabase.change_lineservice')
def LineServiceRegisterView(request, company):
	company = get_object_or_404(Company, id=company)
	form = forms.CompanyUpdateForm(request.POST or None, instance=company)
	formset = forms.LineServiceRegisterFormSet(request.POST or None, instance=company)
	if request.method == 'POST' and form.is_valid() and formset.is_valid():
		form.save()
		formset.save()
		return redirect('moviedatabase:lineservicelistbycompany', company=company.pk)

	categories = BelongsCategory.objects.all()

	context = {
		'company': company,
		'form': form,
		'formset': formset,
		'categories': categories
	}

	return render(request, 'stationdata/lineserviceregister.html', context)

@permission_required('stationdata.add_stationservice')
def StationServiceRegisterView(request, line_service):
	lineservice = get_object_or_404(LineService, pk=line_service)
	lines = Line.objects.filter(company=lineservice.company)
	formset = forms.StationServiceRegisterFormset(request.POST or None, instance=lineservice)
	if request.method == 'POST' and formset.is_valid():
		formset.save()
		stationservices = StationService.objects.filter(line_service=lineservice)
		prefs = Prefecture.objects.none()
		lines = Line.objects.none()
		for stationservice in stationservices:
			if stationservice.group_station_service == None:
				stationservice.group_station_service = stationservice
				stationservice.save()
			if stationservice.station.pref:
				prefs |= Prefecture.objects.filter(pk=stationservice.station.pref.pk)
			lines |= Line.objects.filter(pk=stationservice.station.line.pk)
		for pref in prefs:
			lineservice.prefs.add(pref)
		for line in lines:
			lineservice.line.add(line)
		return redirect('moviedatabase:movielistbylineservice', line_service=lineservice.pk)

	context = {
		'lineservice': lineservice,
		'lines': lines,
		'formset': formset
	}

	return render(request, 'stationdata/stationserviceregister.html', context)

@permission_required('stationdata.change_line')
def lineprefset(request):
	stations = Station.objects.all()
	for station in stations:
		line = station.line
		pref = station.pref
		line.prefs.add(pref)

	return render(request, 'stationdata/upload.html')

@permission_required('stationdata.change_lineservice')
def lineserviceprefset(request):
	stationservices = StationService.objects.all()
	for stationservice in stationservices:
		if stationservice.line_service and stationservice.station:
			line = stationservice.line_service
			pref = stationservice.station.pref
			line.prefs.add(pref)

	return render(request, 'stationdata/upload.html')

@permission_required('stationdata.change_lineservice')
def lineservicelineset(request):
	stationservices = StationService.objects.all()
	for stationservice in stationservices:
		lineservice = stationservice.line_service
		line = stationservice.station.line
		lineservice.line.add(line)
	return render(request, 'stationdata/upload.html')