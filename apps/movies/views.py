from django.views import generic
from django.http import Http404
from django.http import HttpResponse

from .api import MovieApi
from .api import ImdbActorApi
from .api import ImdbMovieApi


class IndexView(generic.TemplateView):
    '''Index page'''
    template_name = 'movies/index.html'
    actors = None
    movies = None

    def get(self, request, *args, **kwargs):
        self.api = MovieApi().fetch(request)
        return super().get(self.api.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['actors'] = self.api.get_actor_list()
        kwargs['movies'] = self.api.get_movie_list()
        kwargs['locations'] = self.api.get_location_list()
        kwargs['random_fact'] = self.api.get_random_fun_fact()
        return kwargs


class ActorView(generic.TemplateView):
    '''Actor page'''
    template_name = 'movies/actor.html'
    actor = None
    keyword_name = 'name'

    def get(self, request, *args, **kwargs):
        self.actor = request.GET.get('name')
        if self.actor:
            # Get location information based on actor
            api = MovieApi().fetch(request)
            api.filter(actor=self.actor)
            self.objects = api.get_objects()
            if not self.objects:
                raise Http404('Data not available for this actor')
            # Get profile picure of actor from IMDB API
            imdb_api = ImdbActorApi(self.actor)
            imdb_api = imdb_api.fetch(request)
            self.imdb = imdb_api.get_objects() or None
        else:
            return HttpResponse('Bad request', status=400)
        return super().get(api.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['locations'] = self.objects
        kwargs['actor'] = self.actor.title()
        if self.imdb:
            kwargs['imdb'] = self.imdb[0]
        return kwargs


class MovieView(generic.TemplateView):
    '''Movie page'''
    template_name = 'movies/movie.html'
    title = None

    def get(self, request, *args, **kwargs):
        self.title = request.GET.get('title')
        if self.title:
            api = MovieApi().fetch(self.request)
            api.filter(title=self.title)
            self.objects = api.get_objects()
            if self.objects:
                self.imdb = ImdbMovieApi(self.title)
                self.imdb = self.imdb.filter(
                    year=self.objects[0]['release_year']
                )
                self.imdb = self.imdb.fetch(request)
                self.imdb = self.imdb.get_objects() or None
            else:
                raise Http404('Data not available for this title')
        else:
            return HttpResponse('Bad request', status=400)
        return super().get(api.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        '''Arrange data

        Filter data by location, and then by actor,
        To make sure we have no empty data or duplicates.
        '''
        # Movie locations
        kwargs = super().get_context_data(**kwargs)
        locations = set()
        for obj in self.objects:
            location = obj.get('locations')
            if location:
                locations.add(location)
        kwargs['locations'] = sorted(list(locations))
        kwargs['movie'] = self.objects[0]
        # Movie actors
        actors = set()
        for obj in self.objects:
            for key in obj.keys():
                if key in MovieApi().actor_fields:
                    actor = obj.get(key, None)
                    if actor:
                        actors.add(obj.get(key))
        kwargs['actors'] = sorted(list(actors))
        if self.imdb:
            kwargs['imdb'] = self.imdb[0]
        return kwargs
