from rest_framework import serializers
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from movies.models import Movie, Genre


class GenreRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        data = Genre.objects.get(name=data).id
        return data

    def to_representation(self, instance):
        return instance.name

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreRelatedField(many=True, queryset=Genre.objects.all())
    class Meta:
        model = Movie
        fields = ['url', 'poster', 'name', 'length', 'language', 'release_date', 'description', 'movie_type', 'genre']

