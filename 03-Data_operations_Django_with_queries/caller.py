import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character

# 01 - Pet
def create_pet(name: str, species: str) -> str:
    Pet.objects.create(
        name = name, 
        species=species
    )
    return f"{name} is a very cute {species}!"

# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


# 02 - Artifacts
def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    Artifact.objects.create(
        name = name,
        origin = origin,
        age = age,
        description = description,
        is_magical = is_magical
    )
    return f"The artifact {name} is {age} years old!"

def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()


# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))

# print(create_artifact('Crystal Amulet', 'Mystic Forest', 300, 'A magical amulet believed to bring good fortune', True))


# 03 - Location
def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')
    
    return '\n'.join([str(loc) for loc in locations])


def new_capital() -> None:
    # Location.objects.filter(id=1).update(is_capital = True)
    location = Location.objects.first()
    location.is_capital = True
    location.save()

def get_capitals():
    return Location.objects.values('name').filter(is_capital = True)


def delete_first_location() -> None:
    Location.objects.first().delete()


# print(show_all_locations())
# print(new_capital())
# print(get_capitals())


# 04 - Car

def apply_discount() -> None:
    cars = Car.objects.all()
    for car in cars:
        price = float(car.price)
        # cast year to str, map str to int
        percentage_off = sum(map(int, str(car.year))) / 100
        discount = price * percentage_off
        car.price_with_discount = price - discount
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gte=2020).values('model', 'price', 'price_with_discount')


def delete_last_car() -> None:
    Car.objects.last().delete()

# apply_discount()
# print(get_recent_cars())


# 05 - Task Encoder
def show_unfinished_tasks() -> str:
    unfinished_tasks = Task.objects.all().filter(is_finished=False)
    return '\n'.join([str(task) for task in unfinished_tasks])


def complete_odd_tasks() -> None:
    Task.objects.filter(id__iregex='^\d*[13579]$').update(is_finished=True)


def encode_and_replace(text: str, task_title: str) -> None:
    # get the char from text ascii symbols - 3. (Z = 90. 87 = W)
    new_text = ''.join([chr(ord(char)-3) for char in text])

    Task.objects.filter(title=task_title).update(description=new_text)
        


# print(show_unfinished_tasks())
# complete_odd_tasks()
# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")


# 06 - Hotel rooms
def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(id__iregex='^\d*[02468]$', room_type='Deluxe')
    return '\n'.join(str(room) for room in deluxe_rooms)


def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.all().order_by("id")
    previous_room_capacity=None
    for room in rooms:
        if not room.is_reserved:
            continue
        if previous_room_capacity:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id
        
        previous_room_capacity = room.capacity
        
        room.save()


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()
    if last_room.is_reserved:
        last_room.delete()


# print(get_deluxe_rooms())
# increase_room_capacity()
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=101).is_reserved)
# delete_last_room()


# 07 - Character
def update_characters() -> None:
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3, 
        intelligence=F('intelligence') - 7
    )
    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2, 
        dexterity=F('dexterity') + 4
    )
    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character: Character, second_character: Character) -> None:
    fusion_level = (first_character.level + second_character.level) // 2
    fusion_strength = (first_character.strength + second_character.strength) * 1.2
    fusion_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    fusion_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    if first_character.class_name in ['Mage', 'Scout']:
        fusion_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        fusion_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name = 'Fusion',
        level = fusion_level,
        strength = fusion_strength,
        dexterity = fusion_dexterity,
        intelligence = fusion_intelligence,
        hit_points = first_character.hit_points + second_character.hit_points,
        inventory = fusion_inventory
    )
    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()


# update_characters()

# character1 = Character.objects.create(
#     name="Gandalf",
#     class_name="Mage",
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory="Staff of Magic, Spellbook",
# )

# character2 = Character.objects.create(
#     name="Hector",
#     class_name="Warrior",
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory="Sword of Troy, Shield of Protection",
# )

# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()

# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)
