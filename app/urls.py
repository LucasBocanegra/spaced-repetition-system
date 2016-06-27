from django.conf.urls import  include,url
from . import  views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^mydecks/', views.my_decks, name='my_decks'),
    url(r'^deck/new/$', views.deck_new, name='deck_new'),
    url(r'^user/new/$', views.user_new, name='user_new'),
    url(r'^deck/(?P<pk>[0-9]+)/edit/$', views.deck_edit, name='deck_edit'),
    url(r'^deck/(?P<pk>[0-9]+)/detail/$', views.deck_detail, name='deck_detail'),
    url(r'^deck/(?P<pk>[0-9]+)/delete/$', views.deck_delete, name='deck_delete'),
    url(r'^cards/init/(?P<pk>[0-9]+)$', views.init_review, name='init_review'),

]