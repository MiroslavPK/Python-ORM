import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from django.db.models import Q, F, Count, Avg
from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None) -> str:
    if search_name is None and search_nationality is None:
        return ""

    query = Q()
    query_name = Q(full_name__icontains = search_name)
    query_nationality = Q(nationality__icontains = search_nationality)

    if search_name is not None and search_nationality is None:
        query = query_name
    elif search_name is None:
        query = query_nationality
    else:
        query = query_name & query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    return '\n'.join(
        f'Director: {director.full_name}, '\
        f'nationality: {director.nationality}, '\
        f'experience: {director.years_of_experience}'
        for director in directors)


def get_top_director() -> str:
    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ''

    return f'Top Director: {director.full_name}, movies: {director.movie_count}.'


def get_top_actor() -> str:
    actor = Actor.objects.prefetch_related('starring_movies') \
        .annotate(
        movies_count=Count('starring_movies'),
        movies_avg_rating=Avg('starring_movies__rating')) \
        .order_by('-movies_count', 'full_name') \
        .first()

    if not actor or not actor.movies_count:
        return ''

    movies = ", ".join(movie.title for movie in actor.starring_movies.all() if movie)

    return f'Top Actor: {actor.full_name}, '\
           f'starring in movies: {movies}, '\
           f'movies average rating: {actor.movies_avg_rating:.1f}'


def get_actors_by_movies_count() -> str:
    actors = Actor.objects.annotate(
        movies_count=Count('actors_in_movies')
    ).filter(
        movies_count__gt=0
    ).order_by(
        '-movies_count', 
        'full_name'
    )[:3]

    if not actors:
        return ''
    
    return '\n'.join(
        f'{actor.full_name}, participated in {actor.movies_count} movies' 
        for actor in actors
    )


def get_top_rated_awarded_movie() -> str:
    movie = Movie.objects.filter(
        is_awarded=True
    ).order_by(
        '-rating',
        'title'
    ).first()

    if not movie:
        return ''
    
    star_actor = movie.starring_actor.full_name if movie.starring_actor else 'N/A'
    cast = ', '.join(actor.full_name for actor in movie.actors.order_by('full_name'))

    return  f'Top rated awarded movie: {movie.title}, '\
            f'rating: {movie.rating}. '\
            f'Starring actor: {star_actor}. '\
            f'Cast: {cast}.'


def increase_rating() -> str:
    movies = Movie.objects.filter(
        is_classic=True,
        rating__lt=10.0,
    ).update(
        rating = F('rating') + 0.1
    )

    if movies == 0:
        return 'No ratings increased.'

    return f'Rating increased for {movies} movies.'
