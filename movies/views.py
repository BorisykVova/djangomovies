from django.shortcuts import redirect
from django.views.generic.base import View
from django.core.handlers.wsgi import WSGIRequest
from django.views.generic import ListView, DetailView

from .models import Movie
from .forms import ReviewForm


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


class AddReview(View):
    """Add new review of movie"""

    def post(self, request: WSGIRequest, pk: int):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            parent_id = request.POST.get('parent', None)
            if parent_id:
                form.parent_id = int(parent_id)
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())
