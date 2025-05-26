from django.db.models.aggregates import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from cinemas.models import Cinema, CinemaHall, Seat, ShowTime, Booking
from cinemas.api.serializers import CinemaSerializer, CinemaHallsSerializer, SeatSerializer, ShowTimeSerializer, \
    BookingSerializer


# Create your views here.
class CinemaViewSet(viewsets.ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
    permission_classes = (IsAdminUser,)


class CinemaHallsViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallsSerializer
    permission_classes = (IsAdminUser,)

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
    search_fields = ['number']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    # powiązanie linków cinema_hall -> seats
    def get_queryset(self):
        queryset = super().get_queryset()
        cinema_hall = self.request.query_params.get('cinema') # parametr z link
        if cinema_hall:
            queryset = queryset.filter(cinema_hall_id=cinema_hall)
        return queryset


class ShowTimeViewSet(viewsets.ModelViewSet):
    queryset = ShowTime.objects.all()
    serializer_class = ShowTimeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAdminUser,)
    search_fields = ['id']


class statGetTicketSold(APIView):
    permission_classes = [IsAdminUser]
    search_fields = ['show_time__name']

    def get(self, request):
        show_time_id = request.query_params.get('show_time_id')

        qs = Booking.objects.filter(payment_status=True).select_related('show_time__movie')

        if show_time_id:
            qs = qs.filter(show_time_id=show_time_id)

        data = (
            qs
            .values('show_time_id', 'show_time__name', 'show_time__movie__name', 'show_time__start_time')
            .annotate(total_sold=Count('id'))
            .order_by('-total_sold')
        )

        return Response(data)