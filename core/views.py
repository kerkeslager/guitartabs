from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

def index(request):
    context = { 'page': 'home' }
    return render(request, 'core/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('tabs:index')

    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def privacy_policy(request):
    context = { 'page': 'privacy_policy' }
    return render(request, 'core/privacy_policy.html')
