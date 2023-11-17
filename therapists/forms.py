from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from .models import Appointment
from django.forms.widgets import DateTimeInput



class AppointmentForm(forms.ModelForm):
    
   

    class Meta:
        model = Appointment
        fields = ['therapist', 'date_and_time', 'additional_info']
        widgets = {
            'date_and_time': DateTimePickerInput(options={
                'format': 'YYYY-MM-DD HH:mm',  
                'showTodayButton': True,
            }),
        }