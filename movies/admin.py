from typing import List, Tuple, Optional

from django import forms
from django.contrib import admin
from django.db.models import QuerySet
from django.utils.safestring import mark_safe
from django.core.handlers.wsgi import WSGIRequest
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Genre, Movie, MoviesShots, Actor, RatingStart, Rating, Reviews


# Register your models here.


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Description')

    class Meta:
        model = Movie
        fields = '__all__'


READONLY_FIELDS = (
    'name',
    'email',
    'text',
    'parent',
    'movie',
)


class ObjImageShow:
    def get_image(self, obj):
        if isinstance(obj, Movie):
            src = obj.poster.url
        else:
            src = obj.image.url

        return mark_safe(f'<img src={src} width="100" height="90">')

    get_image.short_description = 'Image'


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


class MovieShotsInlines(admin.TabularInline, ObjImageShow):
    model = MoviesShots
    extra = 1

    readonly_fields = (
        'get_image',
    )


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin, ObjImageShow):
    save_on_top = True
    save_as = True
    form = MovieAdminForm

    inlines = (
        MovieShotsInlines,
        ReviewInlines,
    )

    actions = (
        'publish',
        'unpublish',
    )

    list_display = (
        'title',
        'category',
        'url',
        'draft',
        'get_image',
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

    list_editable = (
        'draft',
    )
    readonly_fields = (
        'get_image',
    )
    fieldsets = (
        group_fields(
            ('title', 'tagline'),
            group=True,
        ),
        group_fields(
            ('description', ),
        ),
        group_fields(
            ('poster', 'get_image'),
            group=True
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

    def unpublish(self, request: WSGIRequest, queryset: QuerySet):
        """Unpublish this movie"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 row was unpublished.'
        else:
            message_bit = f'{row_update} rows were unpublished.'

        self.message_user(request, message_bit)

    def publish(self, request: WSGIRequest, queryset: QuerySet):
        """Publish this movie"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 row was published.'
        else:
            message_bit = f'{row_update} rows were published.'

        self.message_user(request, message_bit)

    publish.short_description = 'Publish'
    publish.allowed_permission = (
        'change',
    )

    unpublish.short_description = 'Unpublish'
    unpublish.allowed_permission = (
        'change',
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
class MoviesShotsAdmin(admin.ModelAdmin, ObjImageShow):
    list_display = (
        'title',
        'movie',
        'get_image',
    )
    list_display_links = (
        'title',
    )

    readonly_fields = (
        'get_image',
    )


@admin.register(Actor)
class ActorMovies(admin.ModelAdmin, ObjImageShow):
    list_display = (
        'name',
        'age',
        'get_image',
    )
    list_display_links = (
        'name',
    )
    readonly_fields = (
        'get_image',
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


admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'
