# Generated by Django 4.2.4 on 2023-10-28 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_exercise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
