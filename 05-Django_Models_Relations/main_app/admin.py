from django.contrib import admin

from main_app.models import Car

# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("model", "year", "owner", "car_details")

    @staticmethod
    def car_details(car: Car) -> str:
        try:
            owner = car.owner.name
        except AttributeError:
            owner = "No owner"
        
        try:
            reg = car.registration.registration_number
        except AttributeError:
            reg = "No registration number"

        return f"Owner: {owner}, Registration: {reg}"

    
    car_details.short_description = "Car Details"


