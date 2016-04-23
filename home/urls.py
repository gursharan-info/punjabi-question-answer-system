from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^interests/$', views.interests, name='interests'),
    url(r'^about/$', views.about, name='about'),
    url(r'^academic-professional/$', views.academic, name='academic-professional'),
    url(r'^personal/$', views.personal, name='personal'),
]