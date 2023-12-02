from django.core.exceptions import ValidationError


def validate_fruit_name(value):
    for char in value:
        if not char.isalpha():
            raise ValidationError("Fruit name should contain only letters!")