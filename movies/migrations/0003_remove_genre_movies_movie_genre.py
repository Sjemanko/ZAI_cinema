# Generated by Django 5.2.1 on 2025-05-19 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_remove_movie_genre_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='Movies',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(to='movies.genre'),
        ),
    ]
