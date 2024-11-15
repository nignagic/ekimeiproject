from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy

from ..models import *

class NameCreate(PermissionRequiredMixin, generic.CreateView):
	model = Name
	fields = '__all__'
	permission_required = ('moviedatabase.add_name')
	template_name = "moviedatabase/edit_setting/name_form.html"
	success_url = reverse_lazy('moviedatabase:top')

class PopupNameCreate(NameCreate):
	def form_valid(self, form):
		name = form.save()
		context = {
			'object_name': str(name),
			'object_pk': name.pk,
			'function_name': 'add_name'
		}
		return render(self.request, 'moviedatabase/edit_setting/close_name.html', context)


@permission_required('moviedatabase.add_movie')
def popup_parent_movie_setting(request):
	if request.method == 'POST':
		context = {
			'movie_list': request.POST['selected-movie-list'],
			'movie_type': "parent"
		}
		return render(request, 'moviedatabase/edit_setting/close_movie_setting.html', context)

	channels = YoutubeChannel.objects.all()
	movies = Movie.objects.all()

	context = {
		'channels': channels,
		'movies': movies,
		'movie_type': "parent"
	}

	return render(request, 'moviedatabase/edit_setting/movie_setting.html', context)

@permission_required('moviedatabase.add_movie')
def popup_related_movie_setting(request):
	if request.method == 'POST':

		context = {
			'movie_list': request.POST['selected-movie-list'],
			'movie_type': "related"
		}
		return render(request, 'moviedatabase/edit_setting/close_movie_setting.html', context)

	channels = YoutubeChannel.objects.all()
	movies = Movie.objects.all()

	context = {
		'channels': channels,
		'movies': movies,
		'movie_type': "related"
	}

	return render(request, 'moviedatabase/edit_setting/movie_setting.html', context)

@permission_required('moviedatabase.add_movie')
def popup_participant_setting(request):
	if request.method == 'POST':

		context = {
			'participant_list': request.POST['selected-participant-list'],
		}
		return render(request, 'moviedatabase/edit_setting/close_participant_setting.html', context)

	creators = Creator.objects.all()
	names = Name.objects.all()

	context = {
		'creators': creators,
		'names': names,
	}

	return render(request, 'moviedatabase/edit_setting/participant_setting.html', context)
