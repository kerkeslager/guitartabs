from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('<int:user_id>', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('password_changed/', views.password_changed, name='password_changed'),
]
