from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.find, name='find'),
    path('create', views.create, name='create'),
    path('details', views.details, name='details'),
    path('finalize', views.finalize, name='finalize'),
    path('execute', views.execute, name='execute'),
    path('send_execute', views.send_execute, name='send_execute'),
    path('select_match', views.select, name='select_match'),
    path('activate_streamer', views.activate, name='activate_streamer'),
    path('streamer', views.streamer, name='streamer'),
    path('pwd', views.change_password, name='pwd'),
    path('history', views.history, name='history')
    
]