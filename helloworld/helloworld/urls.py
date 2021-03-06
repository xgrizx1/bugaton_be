"""helloworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views
from . import views2

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index, name='index'),
    url(r'^ls/', views.ls, name='ls'),
    url(r'^getLists/', views.getLists, name='getLists'),
    url(r'^getTimestamp/', views.getTimestamp, name='getTimestamp'),
    url(r'^gitClone/', views.gitClone, name='gitClone'),
    url(r'^git/hooks', views.hooks, name='hooks'),
    url(r'^getAverageMoodsWeekly', views.getAverageMoodsWeekly, name='getAverageMoodsWeekly'),
    url(r'^duck/record-event', views2.recodEvent, name='recodEvent'),
    url(r'^post1/', views.post1, name='post1'),
    url(r'^rateDay/', views.rateDay, name='rateDay'),
    url(r'^getAverageEventsWeekly/', views.getAverageEventsWeekly, name='getAverageEventsWeekly'),
    url(r'^getUsers/', views.getUsers, name='getUsers'),
    url(r'^getProjects/', views.getProjects, name='getProjects'),
]
