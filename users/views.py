from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from tabs import models as tab_models

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

def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    tabs = tab_models.Tab.objects.filter(user=user)

    context = {
        'tabs': tabs,
        'user': user
    }

    return render(request, 'users/profile.html', context)
