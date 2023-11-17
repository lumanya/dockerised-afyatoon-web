from django.urls import path

from .views import therapist_page, book_appointment, appointment_success


urlpatterns = [
    path('', therapist_page, name='therapists'),
    path('appointment/<int:therapist_id>/', book_appointment, name='appointment'),
    path('appointment_succcess/', appointment_success, name='appointment_succcess')
]