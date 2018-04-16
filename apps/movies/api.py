import requests
from urllib.parse import urlencode
from random import randint


class BaseApi:
    '''Defines the base API
    
    I want to reuse this caching logic on other APIs.
    '''
    api_endpoint = None
    cache_name = None
    objects = None
    request = None

    def fetch(self, request):
        self.request = request
        is_cached = (self.cache_name in request.session)
        if not is_cached:
            response = requests.get(self.api_endpoint)
            if response.status_code == 200:
                self.request.session[self.cache_name] = response.json()
                # Let it expire after 30 days
                self.request.session.set_expiry(86400 * 30)
        self.objects = self.request.session.get(self.cache_name)
        return self

    def get_objects(self):
        '''Outputs the object list'''
        return self.objects


class MovieApi(BaseApi):
    api_endpoint = 'https://data.sfgov.org/resource/wwmu-gmzc.json'
    cache_name = 'movie_api'
    actor_fields = ('actor_1', 'actor_2', 'actor_3')

    def fetch(self, request):
        '''Fetch objects and takes out rows without location data'''
        super().fetch(request)
        objects = []
        if self.objects:
            for row in self.objects:
                if row.get('locations'):
                    objects.append(row)
        self.objects = objects
        return self

    def filter(self, actor=None, title=None,
               location=None, has_fun_facts=False):
        '''Defines all filtering methods'''
        if actor:
            self.filter_by_actor(actor)
        if title:
            self.filter_by_title(title)
        if location:
            self.filter_by_location(location)
        if has_fun_facts:
            self.has_fun_facts()
        return self

    def filter_by_actor(self, actor):
        '''Filters all the rows with matching actor
        
        Each row with a match should have a location data available too.
        '''
        objects = []
        for row in self.objects:
            for k, v in row.items():
                if k in self.actor_fields:
                    if v.lower() == actor.lower():
                        objects.append(row)
        self.objects = objects
        return self

    def filter_by_title(self, title):
        '''Filters all the rows with matching movie title
        
        Each row with a match should have a location data available too.
        '''
        objects = []
        for row in self.objects:
            if row.get('title'):
                if row.get('title').lower() == title.lower():
                    objects.append(row)
        self.objects = objects
        return self

    def filter_by_location(self, location):
        '''Filters all the rows with matching location
        
        Location must be a case-insensitive exact match.
        '''
        objects = []
        for row in self.objects:
            if row.get('locations').lower() == location.lower():
                objects.append(row)
        self.objects = objects
        return self

    def has_fun_facts(self):
        '''Filter all the rows with fun facts'''
        objects = []
        for row in self.objects:
            if row.get('fun_facts'):
                objects.append(row)
        self.objects = objects
        return self

    def get_random_fun_fact(self):
        '''Gets the fun fact from a random location'''
        self.has_fun_facts()
        return self.objects[randint(0, len(self.objects) - 1)]

    def get_movie_list(self):
        '''List movies'''
        movie_set = set()
        for location in self.objects:
            movie_set.add(location.get('title'))
        return sorted(list(movie_set))

    def get_actor_list(self):
        '''List actors'''
        actor_set = set()
        for location in self.objects:
            for k, v in location.items():
                if k in self.actor_fields:
                    actor_set.add(v)
        return sorted(list(actor_set))

    def get_location_list(self):
        '''List locations'''
        location_set = set()
        for row in self.objects:
            location = row.get('locations')
            if location not in location_set:
                location_set.add(location)
        return sorted(list(location_set))


class ImdbActorApi(BaseApi):
    '''IMDB API

    API for retrieving actor's imdb information.
    '''
    api_endpoint = None
    cache_name = None
    objects = None
    request = None
    query_params = {}

    def __init__(self, actor_name=None):
        self.query_params['name'] = actor_name.lower()

    def fetch(self, request):
        uri = self.get_uri()
        print(uri)
        self.cache_name = uri
        self.api_endpoint = uri
        return super().fetch(request)

    def get_uri(self):
        return 'http://www.theimdbapi.org/api/find/person?{}'.format(
            urlencode(self.query_params),
        )


class ImdbMovieApi(BaseApi):
    '''IMDB API

    API for retrieving a movie's imdb information.
    '''
    api_endpoint = None
    cache_name = None
    objects = None
    request = None
    query_params = {}

    def __init__(self, movie_title=None):
        self.query_params['title'] = movie_title.lower()

    def fetch(self, request):
        uri = self.get_uri()
        print(uri)
        self.cache_name = uri
        self.api_endpoint = uri
        return super().fetch(request)

    def get_uri(self):
        return 'http://www.theimdbapi.org/api/find/movie?{}'.format(
            urlencode(self.query_params),
        )

    def filter(self, year=None):
        if year:
            self.query_params['year'] = year
        return self
