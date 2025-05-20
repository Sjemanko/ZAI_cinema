from django.contrib.auth.models import User
from django.db import models

from movies.models import Movie

# Create your models here.
class Cinema(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f'{self.name, self.location, self.phone_number, self.email}'


class CinemaHall(models.Model):
    name = models.CharField(max_length=100)
    hall_number = models.PositiveSmallIntegerField(blank=True, null=True)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.cinema.name, self.cinema.location, self.name, self.hall_number}'


class Seat(models.Model):
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, blank=True, null=True)
    number = models.PositiveSmallIntegerField()

    class SeatType(models.TextChoices):
        VIP = "VIP"
        STANDARD = "STANDARD"
        PROMO = "PROMO"
        WHEELCHAIR = "WHEELCHAIR"
        SUPER_PROMO = "SUPER_PROMO"

    seat_type = models.CharField(choices=SeatType.choices, default=SeatType.STANDARD)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('cinema_hall', 'number')

    def __str__(self):
        return f'{self.cinema_hall.cinema.location, self.cinema_hall.name, self.number, str(self.seat_type)}'


class ShowTime(models.Model):
    name = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True)
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name, self.movie.name, self.cinema_hall.name, self.start_time, self.end_time, self.ticket_price}'


class Booking(models.Model):
    show_time = models.ForeignKey(ShowTime, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, blank=True, null=True)
    purchase_date = models.DateTimeField()

    def __str__(self):
        return f'{self.show_time.name, self.user.first_name, self.seat.number, self.seat.seat_type, self.show_time.ticket_price}'