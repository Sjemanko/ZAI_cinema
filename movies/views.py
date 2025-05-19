from django.shortcuts import render
from rest_framework import viewsets, permissions

from movies.models import Movie
from movies.serializers import MovieSerializer


# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer