# Generated by Django 5.2 on 2025-05-03 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scheduler', '0016_alter_appointments_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='payment',
            field=models.CharField(choices=[('premium', 'Premium'), ('standard', 'Standard'), ('basic', 'Basic')], max_length=10, null=True),
        ),
    ]
