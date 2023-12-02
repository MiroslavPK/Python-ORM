from django.db import models
from django.core.validators import MinLengthValidator
from fruitipediaApp.fruits.validators import validate_fruit_name


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    def __str__(self) -> str:
        return self.name


class Fruit(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(2),
            validate_fruit_name
        ]
    )

    image_url = models.URLField()

    description = models.TextField()

    nutrition = models.TextField(
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='fruits',
    )
