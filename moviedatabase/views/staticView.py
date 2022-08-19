import datetime
import pytz
from django.shortcuts import render

from pure_pagination.mixins import PaginationMixin

from ..models import *
from .. import forms

from django.views import generic
from django.contrib.auth.views import (
	LoginView, LogoutView
)

import environ
env = environ.Env()
env.read_env('.env')

import twitter

def getTodayMovies():
	now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
	m = Movie.objects.filter(published_at_month=now.month, published_at_day=now.day)
	
	return m

class Top(generic.ListView):
	model = Movie
	template_name = 'moviedatabase/top.html'

	def get_context_data(self):
		movies = Movie.objects.all().exclude(is_active=False)[:6]
		update_list = MovieUpdateInformation.objects.all()[:10]
		notice_list = NoticeInformation.objects.all()[:10]
		top_img = TopImage.objects.all().order_by("?").first()

		context = {
			'top_img': top_img,
			'movie_list': movies,
			'todaymovie': getTodayMovies().order_by("?").first(),
			'today': timezone.now(),
			'update_list': update_list,
			'notice_list': notice_list
		}

		return context

class NoticeList(PaginationMixin, generic.ListView):
	model = NoticeInformation
	paginate_by = 30
	template_name = 'moviedatabase/notice/notice_list.html'

class UpdateList(PaginationMixin, generic.ListView):
	model = MovieUpdateInformation
	paginate_by = 30
	template_name = 'moviedatabase/notice/update_list.html'

class NoticeDetail(generic.DetailView):
	model = NoticeInformation
	template_name = 'moviedatabase/notice/notice_detail.html'

class Login(LoginView):
	form_class = forms.LoginForm
	template_name = 'moviedatabase/login.html'

class Logout(LogoutView):
	template_name = 'moviedatabase/logout.html'

def Mypage(request):
	updateinformations = MovieUpdateInformation.objects.filter(user=request.user)

	context = {
		'updateinformations': updateinformations,
		'user': request.user
	}

	return render(request, 'moviedatabase/mypage.html', context)

def Terms(request):
	# # 取得したキーとアクセストークンを設定する
	# auth = twitter.OAuth(consumer_key=env('API_KEY'),
	# 					consumer_secret=env('API_KEY_SECRET'),
	# 					token=env('ACCESS_TOKEN'),
	# 					token_secret=env('ACCESS_TOKEN_SECRET'))

	# t = twitter.Twitter(auth=auth)

	# # twitterへメッセージを投稿する
	# t.statuses.update(status="あー")

	return render(request, 'moviedatabase/static-page/terms.html')

def Privacy(request):
	return render(request, 'moviedatabase/static-page/privacy.html')

def Update(request):
	return render(request, 'moviedatabase/static-page/update.html')

def GuideAccountCreator(request):
	return render(request, 'moviedatabase/static-page/guide-account-creator.html')

def StartUpGuide(request):
	return render(request, 'moviedatabase/static-page/startup-guide.html')

def LineCustomizeGuide(request):
	return render(request, 'moviedatabase/static-page/line-customize-guide.html')