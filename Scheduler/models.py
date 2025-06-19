from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import CustomUser
import uuid

class Appointments(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='appointments_as_user',
        null=True
    )
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    PAYMENT_CHOICES = [
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('basic', 'Basic'),
    ]
    payment = models.CharField(max_length=8, choices=PAYMENT_CHOICES, null=True)
    amount = models.PositiveIntegerField(null=True)
    made_payment = models.BooleanField(default=False)
    request = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    doctor_selected = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'},
        related_name='appointments',
        null=True
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted(ongoing)'),
        ('rejected', 'Rejected'),
        ('ended', 'Ended'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    status_date = models.DateField(null=True, blank=True)
    call_requested = models.BooleanField(default=False)
    appointment_date = models.DateField(null=True, blank=True)
    call_room_url = models.CharField(max_length=255, default='', blank=True)

    def save(self, *args, **kwargs):
        if self.payment == 'premium':
            self.amount = 10000
        elif self.payment == 'standard':
            self.amount = 5000
        elif self.payment == 'basic':
            self.amount = 2000

        if not self.call_room_url:
            unique_url = str(uuid.uuid4())
            self.call_room_url = f"https://meet.jit.si/{unique_url}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ["-date_created"]

class Messages(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)