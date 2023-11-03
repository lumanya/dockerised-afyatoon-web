from django.urls import path

from .views import AboutPageView, ContactUs


urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactUs.as_view(), name='contact'),
]