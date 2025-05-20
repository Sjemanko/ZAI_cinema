from rest_framework import serializers
from rest_framework.reverse import reverse

from cinemas.models import Cinema, CinemaHall, Seat


class CinemaSerializer(serializers.ModelSerializer):
    cinema_halls_urls = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = ['url', 'name', 'location', 'phone_number', 'email', 'cinema_halls_urls',]

    # powiązanie linków cinema -> cinema_halls
    def get_cinema_halls_urls(self, obj):
        request = self.context.get('request')
        return reverse('cinemahall-list', request=request) + f'?cinema={obj.pk}'


class CinemaHallsSerializer(serializers.ModelSerializer):
    cinema_hall_seats_urls = serializers.SerializerMethodField()
    class Meta:
        model = CinemaHall
        fields = ['url', 'name', 'hall_number', 'cinema', 'cinema_hall_seats_urls']

    # powiązanie linków cinema_hall -> seats
    def get_cinema_hall_seats_urls(self, obj):
        request = self.context.get('request')
        return reverse('seat-list', request=request) + f'?cinema_hall={obj.pk}'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'