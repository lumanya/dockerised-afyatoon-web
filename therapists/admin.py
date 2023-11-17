from django.contrib import admin

from .models import Therapist, Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'date_and_time')

admin.site.register(Therapist)
admin.site.register(Appointment, AppointmentAdmin)