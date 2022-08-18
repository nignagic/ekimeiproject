from django.shortcuts import get_object_or_404, render, redirect
from ..models import *
from django.contrib.auth.decorators import permission_required

@permission_required('moviedatabase.add_movieupdateinformation')
def UpdateInformationforCreator(request, creator):
	creator = get_object_or_404(Creator, id=creator)
	info = MovieUpdateInformation.objects.filter(creator=creator)
	if info:
		t = 'U'
	else:
		t = 'C'
		i = MovieUpdateInformation(movie=None, creator=creator, is_create='C', reg_date=timezone.now())
		i.save()

	return redirect('moviedatabase:movielistbycreator', creator=creator.pk, sort='pub', order='n')

def AccountAndCreatorApplicationView(request):
	if (request.user is None):
		return render(request, '403.html')

	context = {
		'user': request.user,
		'creators': Creator.objects.all()
	}

	return render(request, 'moviedatabase/application/account_and_creator.html', context)

def AccountAndCreatorApplicationConfirmView(request, creator):
	if (request.user is None or request.user.creator_applied):
		return render(request, '403.html')
	creator = Creator.objects.get(pk=creator)

	context = {
		'user': request.user,
		'creator': creator
	}

	if request.method == 'POST':
		request.user.creator_applied = True
		request.user.save()
		dealing = request.POST['dealing']
		ac = AccountAndCreatorApplication(user=request.user, creator=creator, reg_date=timezone.now(), dealing=dealing)
		ac.save()
		return render(request, 'moviedatabase/application/account_and_creator_complete.html', context)

	return render(request, 'moviedatabase/application/account_and_creator_confirm.html', context)

@permission_required('moviedatabase.add_youtubechannel')
def ChannelMovieIsExist(request, channel_id):
	channel = get_object_or_404(YoutubeChannel, channel_id=channel_id)
	context = {
		'channel': channel,
		'movies': Movie.objects.filter(channel=channel)
	}
	return render(request, 'moviedatabase/channel_movie_is_exist.html', context)