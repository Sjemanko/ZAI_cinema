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
    # custom field for cost of full booking
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['purchase_date']

    def create(self, validated_data):
        seat = validated_data['seat']

        # Zabezpieczenie: sprawdź czy już zajęte
        if not seat.is_available:
            raise serializers.ValidationError({'seat': 'To miejsce jest już zajęte.'})

        # Ustaw jako zajęte
        seat.is_available = False
        seat.save()

        return super().create(validated_data)

    def validate(self, data):
        seat = data.get('seat')
        show_time = data.get('show_time')
        if seat and show_time and seat.cinema_hall != show_time.cinema_hall:
            raise serializers.ValidationError({
                'seat': 'To miejsce nie należy do hali tego seansu'
            })
        return data