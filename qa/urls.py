from django.conf.urls import url

from . import views

app_name = 'qa'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^comprehension/$', views.comprehensions, name='comprehensions'),
    url(r'^comprehension/(?P<comprehension_id>[0-9]+)/$', views.compdetail, name='compdetail'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.questiondetail, name='questiondetail'),
    url(r'^dictionary/$', views.dictionary, name='dictionary'),
    url(r'^patterns/$', views.patterns, name='patterns'),
    url(r'^questions/$', views.questions, name='questions'),
    url(r'^toppatterns/$', views.top_patterns, name='toppatterns'),
]