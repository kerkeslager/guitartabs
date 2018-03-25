from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('<int:user_id>', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
]
