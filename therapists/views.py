from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from .models import Therapist
from .forms import AppointmentForm

def therapist_page(request):
    therapists = Therapist.objects.all()
    context = {
        'therapists': therapists,
    }
    return render(request, 'therapists/therapists.html', context)

@login_required(login_url='account_login')
def book_appointment(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.therapist = therapist
            appointment.save()
            
            messages.success(request, "Congratulations you have successfully booked an appoitntment")
            return redirect('appointment_succcess')
    else:
        form =AppointmentForm(initial={'therapist': therapist})

    return render(request, 'therapists/book_appointment.html', {'form': form})


def appointment_success(request):
    return render(request, 'therapists/appointment_success.html')







