from django.contrib import admin

from cinemas.models import Cinema, CinemaHall, Seat, Booking, ShowTime
# Register your models here.

admin.site.register(Cinema)
admin.site.register(CinemaHall)
admin.site.register(Seat)
admin.site.register(ShowTime)
admin.site.register(Booking)