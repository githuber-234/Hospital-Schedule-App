# Generated by Django 5.2 on 2025-05-07 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scheduler', '0018_alter_appointments_amount_alter_appointments_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='file',
            field=models.FileField(null=True, upload_to='uploads/'),
        ),
    ]
