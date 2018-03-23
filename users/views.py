from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from tabs import models as tab_models


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    tabs = tab_models.Tab.objects.filter(user=user)

    context = {
        'tabs': tabs,
        'user': user
    }

    return render(request, 'users/profile.html', context)
