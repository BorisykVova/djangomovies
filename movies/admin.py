from .models import Category, Genre, Movie, MoviesShots, Actor, RatingStart, Rating, Reviews

from django.contrib import admin

# Register your models here.

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MoviesShots)
admin.site.register(Actor)
admin.site.register(RatingStart)
admin.site.register(Rating)
admin.site.register(Reviews)

