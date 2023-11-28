from django.core.exceptions import ValidationError


def validate_birth_year(value):
    if not 1900 <= value <= 2005:
        raise ValidationError()


def validate_rating(value):
    if not 1.0 <= value <= 5.0:
        raise ValidationError()