from django.urls import path

from .views import MovieViews, MovieDetailViews


urlpatterns = [
    path('', MovieViews.as_view()),
    path('<str:slug>/', MovieDetailViews.as_view(), name='movie_detail'),
 ]
