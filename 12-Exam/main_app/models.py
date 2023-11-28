from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from main_app.validators import validate_birth_year, validate_rating
from main_app.manager import AuthorManager


class ContentMixin(models.Model):
    content = models.TextField(
        validators=[
            MinLengthValidator(10),
        ],
    )

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        abstract=True


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
        ],
    )

    email = models.EmailField(
        unique=True,
    )

    is_banned = models.BooleanField(
        default=False,
    )

    birth_year = models.PositiveIntegerField(
        validators=[
            validate_birth_year,
            # MinValueValidator(1990),
            # MaxValueValidator(2005),
        ],
    )

    website = models.URLField(
        null=True,
        blank=True
    )

    objects = AuthorManager()

    def __str__(self) -> str:
        return f"Author: {self.full_name}"


class Article(ContentMixin):
    CATEGORY_CHOICES=(
        ("Technology", "Technology"), 
        ("Science", "Science"), 
        ("Education", "Education"),
    )


    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5),
        ],
    )

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default="Technology"
    )

    authors = models.ManyToManyField(
        Author,
        related_name="articles"
    )

    def __str__(self) -> str:
        return f"Article: {self.title}"


class Review(ContentMixin):
    rating = models.FloatField(
        validators=[
            validate_rating
            # MinValueValidator(1.0),
            # MaxValueValidator(5.0),
        ],
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    def __str__(self) -> str:
        return f"Review: {self.id}"