from typing import List, Tuple, Optional

from .models import Category, Genre, Movie, MoviesShots, Actor, RatingStart, Rating, Reviews

from django.contrib import admin

# Register your models here.


READONLY_FIELDS = (
    'name',
    'email',
    'text',
    'parent',
    'movie',
)


def group_fields(fields: Tuple[str, ...], title: str = None,
                 group: bool = False, classes: Optional[Tuple[str]] = None) -> tuple:

    d = {'fields': ((*fields, ), ) if group else fields}
    if classes:
        d['classes'] = classes
    return title, d


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'url',
    )
    list_display_links = (
        'name',
    )


class ReviewInlines(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = READONLY_FIELDS


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'url',
        'draft',
    )
    list_display_links = (
        'title',
        'url',
    )
    list_filter = (
        'category',
        'year',
    )
    search_fields = (
        'title',
        'category__name',
    )
    inlines = [ReviewInlines]
    save_on_top = True
    save_as = True
    list_editable = (
        'draft',
    )
    fieldsets = (
        group_fields(
            ('title', 'tagline'),
            group=True,
        ),
        group_fields(
            ('description', 'poster'),
        ),
        group_fields(
            ('year', 'country', 'word_premiere'),
            group=True,
            title='Premiere',
        ),
        group_fields(
            ('actors', 'directors', 'genres'),
            group=True,
            title='Actors',
            classes=('collapse',),
        ),
        group_fields(
            ('budget', 'fees_in_usa', 'fees_in_word'),
            group=True,
            title='Money',
        ),
        group_fields(
            ('url', 'draft'),
            group=True,
        ),
    )


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'parent',
        'movie',
    )
    readonly_fields = READONLY_FIELDS


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'url',
    )
    list_display_links = (
        'name',
    )


@admin.register(MoviesShots)
class MoviesShotsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'movie',
        'image',
        'description',
    )
    list_display_links = (
        'title',
    )


@admin.register(Actor)
class ActorMovies(admin.ModelAdmin):
    list_display = (
        'name',
        'age',
        'image',
    )
    list_display_links = (
        'name',
    )


@admin.register(RatingStart)
class RatingStartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'value',
    )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'ip',
        'start',
        'movie',
    )
