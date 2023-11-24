from django import forms

from .models import Contact, Subscribe

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class SubscribeForm(forms.ModelForm):
    """Subscribe Form"""
    class Meta:
        model = Subscribe
        fields = ['email']

