import datetime
from datetime import date

from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    """Category of movies"""

    name = models.CharField('Category', max_length=150)
    description = models.TextField('Description')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Actor(models.Model):
    """Actors and Directors"""

    name = models.CharField('Name', max_length=100)
    age = models.PositiveSmallIntegerField('Age', default=0)
    description = models.TextField('Description')
    image = models.ImageField('Image', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Actors and Directors'
        verbose_name_plural = 'Actors and Directors'


class Genre(models.Model):
    """Genre of Movie"""

    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    """Movies"""
    # attributes
    title = models.CharField('Title', max_length=100)
    tagline = models.CharField('Slogan', max_length=100, default='')
    description = models.TextField('Description')
    poster = models.ImageField('Poster', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Release date', default=datetime.datetime.now().year)
    country = models.CharField('Country', max_length=100)
    word_premiere = models.DateField('Premier in word', default=date.today)
    budget = models.PositiveIntegerField('Budget', default=0, help_text='Specify the dollar amount.')
    fees_in_usa = models.PositiveIntegerField('Fees in USA', default=0, help_text='Specify the dollar amount.')
    fees_in_word = models.PositiveIntegerField('Fees in Word', default=0, help_text='Specify the dollar amount.')
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField('Draft', default=False)

    # many to many
    directors = models.ManyToManyField(Actor, verbose_name='director', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='actors', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='genres')

    # Foreign Keys
    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class MoviesShots(models.Model):
    """Movie footage"""

    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description')
    image = models.ImageField('Image', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Movies', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ' Frame from Movie'
        verbose_name_plural = 'Movie footage'


class RatingStart(models.Model):
    """Start of Rating"""

    value = models.PositiveSmallIntegerField('Value', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Start of Rating'
        verbose_name_plural = 'Starts of Rating'


class Rating(models.Model):
    """Rating"""

    ip = models.CharField('IP address', max_length=15)

    # Foreign key
    start = models.ForeignKey(RatingStart, on_delete=models.CASCADE, verbose_name='start')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='movie')

    def __str__(self):
        return f'{self.start} - {self.movie}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Reviews(models.Model):
    """Reviews"""

    email = models.EmailField()
    name = models.CharField('Name', max_length=100)
    text = models.TextField('Message', max_length=5_000)

    # Foreign Key
    parent = models.ForeignKey('self', verbose_name='Parent', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='movie', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
