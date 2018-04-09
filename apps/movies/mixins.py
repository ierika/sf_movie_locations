from .api import MovieApi


class GetApiMixin:
    api_error = None
    keyword_name = None

    def get(self, request, *args, **kwargs):
        keyword = request.GET.get(self.keyword_name)
        if keyword:
            self.api = MovieApi.fetch(request)
        return super().get(self.api.request, *args, **kwargs)
