from django.urls import path
from .views import (
    SignupView, LoginView, MovieListView, ShowListForMovieView,
    BookSeatView, CancelBookingView, MyBookingsView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/<int:movie_id>/shows/', ShowListForMovieView.as_view(), name='movie-shows'),
    path('shows/<int:show_id>/book/', BookSeatView.as_view(), name='book-seat'),
    path('bookings/<int:booking_id>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
    path('my-bookings/', MyBookingsView.as_view(), name='my-bookings'),
]
