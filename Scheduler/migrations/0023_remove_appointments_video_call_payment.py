# Generated by Django 5.2 on 2025-05-15 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Scheduler', '0022_rename_voice_call_payment_appointments_video_call_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointments',
            name='video_call_payment',
        ),
    ]
