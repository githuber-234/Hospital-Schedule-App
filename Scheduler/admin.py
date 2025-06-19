from django.contrib import admin
from .models import Appointments, Messages, Notification


@admin.register(Appointments)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name',
                    'email', 'phone', 'payment', 'amount', 'made_payment', 'call_requested', 'doctor_selected', 'file', 'request',
                    'date_created', 'status', 'status_date', 'appointment_date')

@admin.register(Messages)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'message', 'date_created')

@admin.register(Notification)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'appointment', 'message', 'date_created')
