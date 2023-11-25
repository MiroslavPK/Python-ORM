from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from main_app.manager import DirectorManager



class BasePerson(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2),
        ],
    )

    birth_date = models.DateField(
        default='1900-01-01',
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown',
    )

    class Meta:
        abstract=True



class BaseInfo(models.Model):
    is_awarded = models.BooleanField(
        default=False,
    )

    last_updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract=True



class Director(BasePerson):

    years_of_experience = models.SmallIntegerField(
        validators=[
            MinValueValidator(0)
        ],
        default=0,
    )

    objects = DirectorManager()

    def __str__(self) -> str:
        return f"Director: {self.full_name}"


class Actor(BasePerson, BaseInfo):

    def __str__(self) -> str:
        return f"Actor: {self.full_name}"


class Movie(BaseInfo):
    GENRE_CHOICES = (
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'), 
        ('Other', 'Other')
    )

    title = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(5),
        ],
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=6,
        choices=GENRE_CHOICES,
        default='Other',
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        default=0.0,
    )

    is_classic = models.BooleanField(
        default=False,
    )

    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
        related_name='movie_directors'
    )

    starring_actor = models.ForeignKey(
        Actor,
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name='starring_movies'
    )

    actors = models.ManyToManyField(
        Actor,
        related_name='actors_in_movies'
    )

    def __str__(self) -> str:
        return f"Movie: {self.title}"