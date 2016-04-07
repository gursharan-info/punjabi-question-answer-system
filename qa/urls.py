from django.conf.urls import url

from . import views

app_name = 'qa'
urlpatterns = [
    url(r'^qa$', views.index, name='index'),
    url(r'^qa/comprehension$', views.comprehensions, name='comprehensions'),
    url(r'^qa/comprehension/(?P<comprehension_id>[0-9]+)/$', views.compdetail, name='compdetail'),
    url(r'^qa/question/(?P<question_id>[0-9]+)/$', views.questiondetail, name='questiondetail'),
    url(r'^qa/dictionary/$', views.dictionary, name='dictionary'),
    url(r'^qa/patterns/$', views.patterns, name='patterns'),
    url(r'^qa/toppatterns/$', views.top_patterns, name='toppatterns'),
]