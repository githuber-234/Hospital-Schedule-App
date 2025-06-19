import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Appointments, Messages, Notification
from users.models import CustomUser
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.db.models import Case, When, IntegerField

# View for Home page
def home(request):
    return render(request, 'Scheduler/home.html')

# View for doctor to manage appointments
@login_required
def doctor(request):
    if request.user.role == 'patient':
        return redirect('not_authorized') 

    appointments = Appointments.objects.filter(
    status='pending',
    made_payment=True,
    doctor_selected=request.user
    ).annotate(
    payment_priority=Case(
        When(payment='premium', then=1),
        When(payment='standard', then=2),
        When(payment='basic', then=3),
        output_field=IntegerField(),
    )
    ).order_by('payment_priority')
    return render(request, 'Scheduler/doctor.html', {'appointments': appointments})

def download_file(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)

    if not appointment.file:
        raise Http404("File not found")

    return FileResponse(appointment.file, as_attachment=True)

# Handle appointment action (accept or reject)
def handle_appointment(request, appointment_id):
    if request.method == 'POST':
        action = request.GET.get('action')
        appointment = get_object_or_404(Appointments, id=appointment_id)
        appointment_date = request.POST.get('appointment_date')

        if appointment_date:
            appointment.appointment_date = appointment_date

        if action == 'accept':
            appointment.status = 'accepted'
            appointment.status_date = timezone.now().date()
            appointment.save()

            Notification.objects.create(
                user=appointment.user,
                message=f"Your appointment has been accepted and scheduled for {appointment.appointment_date}.",
                appointment=appointment
            )

        elif action == 'reject':
            appointment.status = 'rejected'
            appointment.status_date = timezone.now().date()
            appointment.save()

            Notification.objects.create(
                user=appointment.user,
                message="Your appointment has been rejected.",
                appointment=appointment
            )

        elif action == 'end':
            appointment.status = 'ended'
            appointment.status_date = timezone.now().date()
            appointment.save()

            Notification.objects.create(
                user=appointment.user,
                message="The Doctor has ended your appointment.",
                appointment=appointment
            )

    return redirect('doctor')


# View for patient to send messages
@login_required
def patient(request):
    if request.user.role == 'doctor':
        return redirect('not_authorized') 

    user = request.user

    if request.method == "POST":
        name = request.POST.get('name')
        email_address = request.POST.get('email')
        message = request.POST.get('message')

        email = EmailMessage(
            subject=f"From {name}",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email_address]
        ) 
        email.send()
        
        Messages.objects.create(
            user=user,
            name=name,
            email=email_address,
            message=message,
        )
        messages.success(request, "Email sent successfully!")
        return redirect('patient')

    return render(request, 'Scheduler/patient.html')

# View for patient to make an appointment
@login_required
def appointment(request):
    if request.user.role == 'doctor':
        return redirect('not_authorized')

    doctors = CustomUser.objects.filter(role='doctor')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        doctor_id = request.POST.get('doctor')
        payment_method = request.POST.get('payment')
        request_text = request.POST.get('request')
        uploaded_file = request.FILES.get('fileUpload')

        doctor = get_object_or_404(CustomUser, id=doctor_id)

        appointment = Appointments.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            payment=payment_method,
            request=request_text,
            file=uploaded_file,
            doctor_selected=doctor,
            user=request.user,
            made_payment=False
        )

        return redirect('payment', appointment_id=appointment.id)

    return render(request, 'Scheduler/appointment.html', {'doctors': doctors})


# View for patient to make payment for appointment
@login_required
def payment(request, appointment_id):
    if request.user.role == 'doctor':
        return redirect('not_authorized')

    appointment = get_object_or_404(Appointments, id=appointment_id, user=request.user)
    doctor = appointment.doctor_selected

    if request.method == 'POST':
        uploaded_file = request.FILES.get('fileUpload')
        if uploaded_file:
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join('uploads', uploaded_file.name)
            with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            appointment.file = file_path


        appointment.made_payment = True
        appointment.save()

        return redirect('confirmation')

    return render(request, 'Scheduler/payment.html', {'appointment': appointment, 'doctor':doctor})


@login_required
def receipt(request):
    if request.user.role == 'doctor':
        return redirect('not_authorized') 

    appointments = Appointments.objects.filter(user=request.user).order_by('-date_created')

    if not appointments.exists():
        messages.info(request, 'You have not made any appointments yet.')
        return redirect('patient')

    return render(request, 'Scheduler/receipt.html', {
        'appointments': appointments
    })

# View for confirmation after appointment creation
@login_required
def confirmation(request):
    if request.user.role == 'doctor':
        return redirect('not_authorized') 
    
    return render(request, 'Scheduler/confirmation.html')

# View for displaying notifications
@login_required
def notifications(request):
    if request.user.role == 'doctor':
        return redirect('not_authorized')
    
    notifications = Notification.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'Scheduler/notifications.html', {'notifications': notifications})

# View for deleting a notification
@require_POST
@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return redirect('notifications')

# View for unauthorized access page
@login_required
def not_authorized(request):
    return render(request, 'Scheduler/not-authorized.html')

@login_required
def appointment_history(request):
    if request.user.role == 'patient':
        return redirect('not_authorized')

    appointments = Appointments.objects.filter(
        doctor_selected=request.user,
        status__in=['accepted', 'rejected', 'ended']
    ).order_by('-status_date')

    return render(request, 'Scheduler/appointment_history.html', {
        'appointments': appointments
    })

# Patient view to request a video call for accepted appointments
@login_required
def patient_request_video_call(request):
    if request.user.role == 'doctor':
        return redirect('not_authorized')
    
    appointments = Appointments.objects.filter(
        user=request.user,
        status__in=['accepted']
    ).order_by('-status_date')

    return render(request, 'Scheduler/patient_request_video_call.html', {
        'appointments': appointments
    })

# View to handle the video call request (when patient clicks "Request Call")
@login_required
def request_video_call(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)

    if appointment.user != request.user:
        return redirect('not_authorized')
    
    if appointment.call_requested:
        messages.warning(request, "You have already requested a video call for this appointment.")
        return redirect('patient_request_video_call')
    
    appointment.call_requested = True
    appointment.save()

    messages.success(request, "Video call request sent to the doctor.")
    return redirect('patient_request_video_call')

# Doctor's view to see video call requests for their appointments
@login_required
def doctor_video_call_requests(request):
    if request.user.role == 'patient':
        return redirect('not_authorized')

    appointments = Appointments.objects.filter(
        doctor_selected=request.user,
        status__in=['accepted'],
        call_requested=True
    ).order_by('-status_date')

    return render(request, 'Scheduler/doctor_video_call_requests.html', {'appointments': appointments})

@login_required
def patient_join_video_call(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    
    return redirect(appointment.call_room_url)

@login_required
def doctor_join_video_call(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    
    if appointment.doctor_selected == request.user:
        return redirect(appointment.call_room_url)

    return redirect('not_authorized')

def ongoing_appointment(request):
    if request.user.role == 'patient':
        return redirect('not_authorized')

    appointments = Appointments.objects.filter(
        doctor_selected=request.user,
        status__in=['accepted']
    ).order_by('-status_date')
    return render(request, 'Scheduler/ongoing_appointment.html', {'appointments': appointments})