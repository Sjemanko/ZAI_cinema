from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class Movie(models.Model):
    name = models.CharField(max_length=100)
    length = models.IntegerField()

    class Language(models.TextChoices):
        ENGLISH = 'ENG', _('English')
        POLISH = 'PL', _('Polish')

    class MovieType(models.TextChoices):
        DUBBING = "DUBBING",
        LECTOR = "LECTOR",
        SUBTITLES = "SUBTITLES",

    language = models.CharField(max_length=100, choices=Language, default=Language.POLISH)
    release_date = models.DateField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    movie_type = models.CharField(max_length=100, choices=MovieType.choices)

    def __str__(self):
        return f'{self.name, self.release_date.__str__(), list(self.genre.all())}'


