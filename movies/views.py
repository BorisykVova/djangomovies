from django.views.generic import ListView, DetailView

from .models import Movie


class MovieViews(ListView):
    """Render list of movies"""

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'
    context_object_name = 'movies_list'


class MovieDescriptionViews(DetailView):
    """Render full description of movie"""

    model = Movie
    slug_field = 'url'
    template_name = 'movies/movie_description.html'
