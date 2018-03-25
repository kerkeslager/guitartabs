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

def change_password(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login') + '?next=' + reverse('users:change_password'))

    if request.method == 'GET':
        change_password_form = forms.ChangePasswordForm()
        context = {
            'change_password_form': change_password_form,
        }
        return render(request, 'users/change_password.html', context)

    if request.method == 'POST':
        change_password_form = forms.ChangePasswordForm(request.POST)

        # We can't (reasonably) do this in the form validation because we don't
        # have access to the request object.
        if not authenticate(request, username=request.user.username, password=change_password_form.data['current_password']):
            change_password_form.add_error('current_password', 'Current password is incorrect')

        # We could do this in the form, but it's easier to have all the validation in one place
        if change_password_form.data['new_password'] != change_password_form.data['confirm_new_password']:
            change_password_form.add_error('confirm_new_password', 'New password confirmation does not match')

        if change_password_form.is_valid():
            user = request.user
            user.set_password(change_password_form.cleaned_data['new_password'])
            user.save()
            return redirect('users:password_changed')

        context = {
            'change_password_form': change_password_form,
        }
        return render(request, 'users/change_password.html', context)

def password_changed(request):
    return render(request, 'users/password_changed.html')
