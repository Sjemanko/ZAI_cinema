from django.utils import timezone
from rest_framework import serializers
from rest_framework.reverse import reverse

from cinemas.api.CustomFields import CustomSeatField
from cinemas.models import Cinema, CinemaHall, Seat, ShowTime, Booking
from movies.api.serializers import MovieSerializer
from movies.models import Movie


class CinemaSerializer(serializers.ModelSerializer):
    cinema_halls_urls = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = ['id', 'url', 'name', 'location', 'phone_number', 'email', 'cinema_halls_urls',]

    # powiązanie linków cinema -> cinema_halls
    def get_cinema_halls_urls(self, obj):
        request = self.context.get('request')
        return reverse('cinemahall-list', request=request) + f'?cinema={obj.id}'


class CinemaHallsSerializer(serializers.ModelSerializer):
    cinema_hall_seats_urls = serializers.SerializerMethodField()
    class Meta:
        model = CinemaHall
        fields = ['id', 'url', 'name', 'hall_number', 'cinema', 'cinema_hall_seats_urls']

    # powiązanie linków cinema_hall -> seats
    def get_cinema_hall_seats_urls(self, obj):
        request = self.context.get('request')
        return reverse('seat-list', request=request) + f'?cinema={obj.pk}'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'


class ShowTimeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(many=False, read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='movie',
        write_only=True
    )
    class Meta:
        model = ShowTime
        fields = ['url', 'movie_id',] + [field.name for field in ShowTime._meta.fields]


class BookingSerializer(serializers.ModelSerializer):
    seat = CustomSeatField(queryset=Seat.objects.all())

    class Meta:
        model = Booking
        fields = ['url'] + [field.name for field in Booking._meta.fields]
        read_only_fields = ['purchase_date']

    def create(self, validated_data):
        seat = validated_data['seat']

        if not seat.is_available:
            raise serializers.ValidationError({'seat': 'To miejsce jest już zajęte.'})

        seat.is_available = False
        seat.save()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        old_seat = instance.seat
        new_seat = validated_data['seat']
        new_payment_status = validated_data['payment_status']


        if new_seat != old_seat:
            if not new_seat.is_available:
                raise serializers.ValidationError({'seat': 'To miejsce jest już zajęte.'})
            old_seat.is_available = True
            old_seat.save()
            new_seat.is_available = False
            new_seat.save()

        if new_payment_status and new_payment_status is True and instance.purchase_date is None:
            instance.purchase_date = timezone.now()
        return super().update(instance, validated_data)

    def validate(self, data):
        seat = data.get('seat')
        show_time = data.get('show_time')
        if seat and show_time and seat.cinema_hall != show_time.cinema_hall:
            raise serializers.ValidationError({
                'seat': 'To miejsce nie należy do hali tego seansu'
            })
        return data