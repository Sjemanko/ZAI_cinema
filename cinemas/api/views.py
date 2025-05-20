from rest_framework import viewsets

from cinemas.models import Cinema, CinemaHall, Seat
from cinemas.api.serializers import CinemaSerializer, CinemaHallsSerializer, SeatSerializer


# Create your views here.
class CinemaViewSet(viewsets.ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer

class CinemaHallsViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallsSerializer

    # powiązanie linków cinema -> cinema_halls
    def get_queryset(self):
        queryset = super().get_queryset()
        cinema_id = self.request.query_params.get('cinema')
        if cinema_id:
            queryset = queryset.filter(cinema_id=cinema_id)
        return queryset

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    # powiązanie linków cinema_hall -> seats
    def get_queryset(self):
        queryset = super().get_queryset()
        cinema_hall_id = self.request.query_params.get('cinema_hall') # parametr z link
        if cinema_hall_id:
            queryset = queryset.filter(cinema_hall_id=cinema_hall_id)
        return queryset