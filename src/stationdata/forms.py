from django.forms import Form, ModelForm, inlineformset_factory
from django import forms
from .models import *

class CompanyRegisterForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = '__all__'

class LineRegisterForm(forms.ModelForm):
	class Meta:
		model = Line
		fields = '__all__'
		widgets = {
			'sort_by_company': forms.TextInput(attrs={
				'class': 'sort_by_company',
			}),
		}

LineRegisterFormset = forms.inlineformset_factory(
	parent_model = Company,
	fk_name = 'company',
	model = Line, 
	form = LineRegisterForm,
	extra = 0,
	can_delete = False
)

class StationRegisterForm(forms.ModelForm):
	class Meta:
		model = Station
		fields = ('group_station_new', 'name', 'name_kana', 'line', 'sort_by_line', 'open_ymd', 'close_ymd', 'pref', 'status')
		widgets = {
			'group_station_new': forms.TextInput(),
			'sort_by_line': forms.TextInput(attrs={
				'class': 'sort_by_line',
			}),
		}

StationRegisterFormset = forms.inlineformset_factory(
	parent_model = Line,
	fk_name = 'line',
	model = Station,
	form = StationRegisterForm,
	extra = 0,
	can_delete = False
)

class StationUpdateForm(forms.ModelForm):
	class Meta:
		model = Station
		fields = ('name', 'line')

class StationServiceUpdateForm(forms.ModelForm):
	class Meta:
		model = StationService
		fields = ('name', 'line_service')

class CompanyUpdateForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = ('name', 'short_name', 'short_name_2', 'name_kana', 'color')

class LineServiceRegisterForm(forms.ModelForm):
	class Meta:
		model = LineService
		fields = ('category', 'name', 'name_sub', 'color', 'sort_by_company', 'status', 'is_formal', 'is_service')
		widgets = {
			'sort_by_company': forms.TextInput(attrs={
				'class': 'sort_by_company',
			}),
		}

LineServiceRegisterFormSet = forms.inlineformset_factory(
	parent_model = Company,
	fk_name = 'company',
	model = LineService,
	form = LineServiceRegisterForm,
	extra = 0,
	can_delete = False
)

class StationServiceRegisterForm(forms.ModelForm):
	class Meta:
		model = StationService
		fields = ('name', 'station', 'line_service', 'numbering_head', 'numbering_symbol', 'numbering_middle', 'numbering_number', 'sort_by_line_service', 'color')
		widgets = {
			'station': forms.HiddenInput(),
			'group_station_service': forms.HiddenInput(),
			'line_service': forms.HiddenInput(),
			'sort_by_line_service': forms.TextInput(attrs={
				'class': 'sort_by_line_service',
			}),
		}

StationServiceRegisterFormset = forms.inlineformset_factory(
	parent_model = LineService,
	fk_name = 'line_service',
	model = StationService,
	form = StationServiceRegisterForm,
	extra = 0,
	can_delete = False
)