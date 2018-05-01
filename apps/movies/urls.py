from django.urls import path

from . import views


app_name = 'movies'


# Standard views
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('actor/', views.ActorView.as_view(), name='actor'),
    path('movie/', views.MovieView.as_view(), name='movie'),
]

# Ajax views
urlpatterns += [
    path('api/movies/locations/',
         views.api_get_locations,
         name='api_get_locations'),
]
