import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# from main_app.models import Shoe
from main_app.models import Person

# print(Shoe.objects.values_list('brand', flat=True).distinct())
print(Person.objects.all())


