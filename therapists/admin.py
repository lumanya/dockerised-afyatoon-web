from django.contrib import admin

from .models import Therapist, Appointment, TimeSlot

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'time_slot')

admin.site.register(Therapist)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(TimeSlot)


