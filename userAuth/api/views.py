from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status, generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cinemas.api.serializers import BookingSerializer, ShowTimeSerializer
from cinemas.models import Booking, ShowTime
from userAuth.api.serializers import UserSerializer, GroupSerializer, ProfileWithBookingSerializer, \
    ProfileCreateSerializer, ProfileSerializer
from userAuth.models import Profile


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]

class ProfileDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileWithBookingSerializer(profile, context={'request': request})
        return Response(serializer.data)

class ProfileCreateView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ProfileCreateSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(ProfileCreateSerializer(profile, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
