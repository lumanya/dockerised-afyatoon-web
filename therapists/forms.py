from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from .models import Appointment
from django.forms.widgets import DateTimeInput



class AppointmentForm(forms.ModelForm):
    
   

    class Meta:
        model = Appointment
        fields = ['therapist', 'time_slot', 'additional_info']
       



    