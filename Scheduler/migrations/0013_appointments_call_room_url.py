# Generated by Django 5.2 on 2025-04-20 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scheduler', '0012_appointments_call_requested'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='call_room_url',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
