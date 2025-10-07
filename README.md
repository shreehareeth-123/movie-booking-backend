# Movie Ticket Booking System (Django + DRF)

This repository is a scaffold for the Backend Intern Assignment:
a Movie Ticket Booking System built with Django and Django REST Framework.

## Features
- Signup & Login using JWT authentication (Simple JWT)
- List movies and shows
- Book a seat for a show
- Cancel a booking
- Swagger API documentation at `/swagger/`

## Tech stack
- Python, Django, Django REST Framework
- djangorestframework-simplejwt for JWT
- drf-yasg for Swagger docs
- SQLite (default)

## Setup (local)
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints
- `POST /api/signup/` → Register a user (username, email, password)
- `POST /api/login/` → Obtain JWT (`username` and `password`)
- `POST /api/token/refresh/` → Refresh JWT
- `GET /api/movies/` → List movies
- `GET /api/movies/<id>/shows/` → List shows for a movie
- `POST /api/shows/<id>/book/` → Book a seat (`seat_number` in JSON body) — requires Authorization: Bearer &lt;token&gt;
- `POST /api/bookings/<id>/cancel/` → Cancel a booking — requires Authorization
- `GET /api/my-bookings/` → List current user's bookings — requires Authorization
- `Swagger UI: /swagger/`

## Booking rules implemented
- Prevent double booking: `unique_together` on `(show, seat_number)` and select_for_update checks.
- Prevent overbooking: compare current booked count vs show.total_seats.
- Cancelling sets booking.status to `cancelled` which frees seat.

## Notes & Next steps / Bonus ideas
- Add API tests for booking flows.
- Improve concurrency handling with retry logic.
- Add pagination, filtering (by date), and admin endpoints for creating movies/shows.
- Add input validation and better error messages.

## Files
- `booking_project/` — Django project
- `movies/` — Django app containing models, serializers, views, urls
- `requirements.txt`
- `README.md`

---
