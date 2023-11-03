from django.shortcuts import render

from django.views.generic import TemplateView


class AboutPageView(TemplateView):
    template_name = 'about.html'

class ContactUs(TemplateView):
    template_name = 'contact.html'
