from django.conf.urls import url
from . import views

app_name = 'partyqueue'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='index'),
    url(r'^all/$', views.all, name='all'),
    url(r'^play/$', views.play, name='play'),
    #url(r'^play_music/$', views.play_music, name='play_music'),
    url(r'^remove/$', views.remove, name='remove'),
    #url(r'^remove_music/$', views.remove_music, name='remove_music'),
    url(r'^watch/$', views.watch, name="watch"),
    url(r'^listen/$', views.listen, name="listen"),
    url(r'^mashup/$', views.mashup, name="mashup"),
]