from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm, SubscribeForm
from .models import Contact


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Thank you for Contacting us")

            return redirect('appointment_succcess')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations you have successfully Subscribed to our newsletter to receive our weekly feed")

            return redirect('appointment_succcess')
    else:
        form = SubscribeForm()

    return render(request, 'about.html', {'form': form})
            
            
                    

