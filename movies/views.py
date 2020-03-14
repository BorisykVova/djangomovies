from django.views.generic import ListView, DetailView

from .models import Movie


class MovieViews(ListView):
    """Render list of movies"""

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'


class MovieDetailViews(DetailView):
    """Render full description of movie"""

    model = Movie
    slug_field = 'url'
    template_name = 'movies/movie_detail.html'
