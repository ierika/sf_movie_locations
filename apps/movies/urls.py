from django.urls import path

from . import views


app_name = 'movies'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('actor', views.ActorView.as_view(), name='actor'),
    path('movie', views.MovieView.as_view(), name='movie'),
]
