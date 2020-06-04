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

class StationRegisterForm(forms.ModelForm):
	class Meta:
		model = Station
		fields = ('name', 'name_kana', 'line', 'sort_by_line', 'open_ymd', 'close_ymd', 'pref', 'status')
		widgets = {
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

class LineServiceRegisterForm(forms.ModelForm):
	class Meta:
		model = LineService
		fields = '__all__'

class CompanyUpdateForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = ('name', 'short_name', 'short_name_2', 'name_kana', 'color')

class LineServiceEditForm(forms.ModelForm):
	class Meta:
		model = LineService
		fields = ('category', 'name', 'name_sub', 'company', 'color', 'prefs', 'sort_by_company')

LineServiceEditFormSet = forms.inlineformset_factory(
	parent_model = Company,
	fk_name = 'company',
	model = LineService,
	form = LineServiceEditForm,
	extra = 0,
	can_delete = False
)

class StationServiceRegisterForm(forms.ModelForm):
	class Meta:
		model = StationService
		fields = '__all__'

StationServiceRegisterFormset = forms.inlineformset_factory(
	parent_model = LineService,
	fk_name = 'line_service',
	model = StationService,
	form = StationServiceRegisterForm,
	extra = 0,
	can_delete = False
)