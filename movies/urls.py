from django.urls import path

from .views import MovieViews, MovieDescriptionViews


urlpatterns = [
    path('', MovieViews.as_view()),
    path('<str:slug>/', MovieDescriptionViews.as_view(), name='movie_description'),
]
