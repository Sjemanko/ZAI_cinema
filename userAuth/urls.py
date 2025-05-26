from django.urls import path

from userAuth.api.views import ProfileDataView, ProfileCreateView, BookingCreateView

urlpatterns = [
    path('profile/', ProfileDataView.as_view(), name='profile_view'),
    path('profile/create/', ProfileCreateView.as_view(), name='profile_create'),
    path('profile/booking/create/', BookingCreateView.as_view(), name='booking_create'),
]