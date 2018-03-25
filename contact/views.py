from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render

from . import forms

def contact(request):
    if request.method == 'GET':
        context = {
            'page': 'contact',
            'contact_form': forms.ContactForm()
        }
        return render(request, 'contact/contact.html', context)

    else:
        form = forms.ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']

            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return render(request, 'contact/success.html')

        context = {
            'contact_form': forms.ContactForm()
        }
        return render(request, 'contact/contact.html', context)
