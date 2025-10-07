# Example commands to create sample data after migrations:
python manage.py shell -c "from movies.models import Movie, Show; m=Movie.objects.create(title='Sample Movie', duration_minutes=120); Show.objects.create(movie=m, screen_name='A', date_time='2030-01-01T18:00:00Z', total_seats=10)"
