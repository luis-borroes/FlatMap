from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'flatmap'

urlpatterns = [
	path('', views.mapsIPSS, name='index'),
	path('about/', views.about, name='about'),

	path('search/', views.listIPSS, name='listIPSS'),
	path('map/', views.mapsIPSS, name='mapsIPSS'),
	path('map/d/<int:dist>', views.mapsIPSSDist, name='mapsIPSSDist'),
	path('map/c/<int:conc>', views.mapsIPSSConc, name='mapsIPSSConc'),
	path('map/f/<int:freg>', views.mapsIPSSFreg, name='mapsIPSSFreg'),

	path('ipss/<int:inst>', views.dispIPSS, name='dispIPSS'),

	path('events/', views.evtsList, name='evtsList'),
	path('news/', views.newsList, name='newsList'),
	path('events/<str:slug>', views.evtsDisp, name='evtsDisp'),
	path('news/<str:slug>', views.newsDisp, name='newsDisp'),
	
	path('genIPSS/', views.genIPSSDatabase, name='genIPSSDatabase'),
]