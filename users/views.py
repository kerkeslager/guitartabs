from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from . import forms
from core import util
from tabs import models as tab_models

def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    tabs = tab_models.Tab.objects.filter(user=user)

    context = {
        'tabs': tabs,
        'user': user
    }

    return render(request, 'users/profile.html', context)

def edit_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login') + '?next=' + reverse('users:edit_profile'))

    if request.method == 'GET':
        user_form = forms.UserForm(model_to_dict(request.user))
        context = {
            'user_form': user_form
        }
        return render(request, 'users/edit_profile.html', context)

    if request.method == 'POST':
        user_form = forms.UserForm({
            **util.params_to_dict(request.POST),
        })

        # We can't (reasonably) do this in the form validation because we don't
        # have access to the request object.
        email = user_form.data.get('email')
        if email and User.objects.exclude(pk=request.user.pk).filter(email=email).count():
            user_form.add_error('email', 'Email is already in use by another user account')

        if user_form.is_valid():
            user = request.user
            user.email = user_form.cleaned_data.get('email')
            user.first_name = user_form.cleaned_data.get('first_name')
            user.last_name = user_form.cleaned_data.get('last_name')
            user.save()
            return HttpResponseRedirect(reverse('users:profile', args=(user.pk,)))

        context = { 'user_form': user_form }
        return render(request, 'users/edit_profile.html', context)
