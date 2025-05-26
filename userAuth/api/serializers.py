from django.contrib.auth.models import Group, User
from django.db import models
from rest_framework import serializers

from cinemas.api.serializers import BookingSerializer
from userAuth.models import Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'},
                                     required=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'password', 'email')


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['user','phone_number']


class ProfileWithBookingSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    total_cost = serializers.SerializerMethodField('sum_tickets')
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bookings', 'total_cost']

    def sum_tickets(self, obj):
        unpaid_bookings = obj.bookings.filter(payment_status=False)
        total = sum(booking.show_time.ticket_price for booking in unpaid_bookings)
        return total


class ProfileCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'phone_number']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile
