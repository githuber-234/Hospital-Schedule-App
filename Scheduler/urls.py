from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patient/', views.patient, name='patient'),
    path('doctor/', views.doctor, name='doctor'),
    path('download/<int:document_id>/', views.download_file, name='download_file'),
    path('appointment_history/', views.appointment_history, name='appointment_history'),
    path('appointment/', views.appointment, name='appointment'),
    path('payment/<int:appointment_id>', views.payment, name='payment'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('receipt/', views.receipt, name='receipt'),
    path('handle-appointment/<int:appointment_id>/', views.handle_appointment, name='handle_appointment'),
    path('ongoing_appointments/', views.ongoing_appointment, name='ongoing_appointments'),
    path('not_authorized/', views.not_authorized, name='not_authorized'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('patient-request-video-call/', views.patient_request_video_call, name='patient_request_video_call'),
    path('patient-request-video-call/<int:appointment_id>', views.request_video_call, name='request_video_call'),
    path('doctor-video-call-requests/', views.doctor_video_call_requests, name='doctor_video_call_requests'),
    path('video-call/join/<int:appointment_id>/', views.patient_join_video_call, name='patient_join_video_call'),
    path('video-call/doctor/join/<int:appointment_id>/', views.doctor_join_video_call, name='doctor_join_video_call'),
]
