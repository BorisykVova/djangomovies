from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.

from .models import Movie


class MovieViews(View):
    """List of movies"""

    def get(self, request):
        movies = Movie.objects.all()
        return render(request,'movies/movies.html', {'movies_list': movies})
