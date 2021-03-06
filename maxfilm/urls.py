"""mysite URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from . import views

app_name = "maxfilm"
urlpatterns = [
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^bookmark/$', views.bookmark, name="bookmark"),
    url(r'^pending/$', views.pending, name="pending"),
    url(r'^viewed/$', views.viewed, name="viewed"),
    url(r'^add/$', views.add, name="add"),
    url(r'^$', views.index, name="index"),
    url(r'^movie/(?P<id>[0-9]+)/$', views.viewMovie, name="viewMovie"),
    url(r'^tv/(?P<id>[0-9]+)/$', views.viewTv, name="viewTv"),
    url(r'^person/(?P<id>[0-9]+)/$', views.viewPerson, name="viewPerson"),
    url(r'^search/$', views.Search, name="Search"),
    url(r'^movies/$', views.Movies, name="Movies"),
    url(r'^tv/$', views.Tv, name="Tv"),
    url(r'^people/$', views.People, name="People"),
]
