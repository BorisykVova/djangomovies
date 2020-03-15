from django.urls import path

from . import views


urlpatterns = [
    path('', views.MovieViews.as_view()),
    path('<str:slug>/', views.MovieDetailViews.as_view(), name='movie_detail'),
    path('review/<int:pk>', views.AddReview.as_view(), name='add_review'),
 ]
