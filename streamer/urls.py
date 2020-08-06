from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.streamer_home, name='home'),
    path('add_match', views.add_match, name='add_match'),
    path('enter_stats', views.enter_stats, name='enter_stats'),
    path('confirm_stats', views.confirm_stats, name='confirm_stats'),
    path('end_stream', views.end_stream, name='end_stream'),
    path('begin_stream', views.begin_stream, name='begin_stream')
]