from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Movie, Show, Booking
from .serializers import (
    SignupSerializer, MovieSerializer, ShowSerializer, BookingSerializer
)

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)

class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (permissions.AllowAny,)

class ShowListForMovieView(generics.ListAPIView):
    serializer_class = ShowSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        movie_id = self.kwargs.get('movie_id')
        return Show.objects.filter(movie_id=movie_id)

class BookSeatView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request, show_id):
        user = request.user
        seat_number = request.data.get('seat_number')
        if seat_number is None:
            return Response({'detail':'seat_number is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seat_number = int(seat_number)
        except ValueError:
            return Response({'detail':'seat_number must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        show = get_object_or_404(Show, pk=show_id)

        if seat_number < 1 or seat_number > show.total_seats:
            return Response({'detail':'seat_number out of range'}, status=status.HTTP_400_BAD_REQUEST)

        # Lock bookings for this show to prevent race conditions
        existing = Booking.objects.select_for_update().filter(show=show, seat_number=seat_number, status='booked').first()
        if existing:
            return Response({'detail':'seat already booked'}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent overbooking: count currently booked seats
        booked_count = Booking.objects.select_for_update().filter(show=show, status='booked').count()
        if booked_count >= show.total_seats:
            return Response({'detail':'no seats available'}, status=status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.create(user=user, show=show, seat_number=seat_number, status='booked')
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CancelBookingView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)
        # Security: only owner can cancel
        if booking.user != request.user:
            return Response({'detail':'cannot cancel others booking'}, status=status.HTTP_403_FORBIDDEN)
        if booking.status == 'cancelled':
            return Response({'detail':'booking already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save()
        return Response({'detail':'booking cancelled'}, status=status.HTTP_200_OK)

class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
