from rest_framework import routers

from cinemas.api.views import CinemaViewSet, CinemaHallsViewSet, SeatViewSet, ShowTimeViewSet, BookingViewSet
from movies.api.views import MovieViewSet
from userAuth.api.views import GroupViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'users', UserViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'cinemas', CinemaViewSet)
router.register(r'cinemahalls', CinemaHallsViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'showtimes', ShowTimeViewSet)

router.register(r'bookings', BookingViewSet)