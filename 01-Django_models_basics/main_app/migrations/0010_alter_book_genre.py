# Generated by Django 4.2.4 on 2023-10-28 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('Fiction', 'Fiction'), ('Non-Fiction', 'Non-Fiction'), ('Science Fiction', 'Science Fiction'), ('Horror', 'Horror')], max_length=20),
        ),
    ]
