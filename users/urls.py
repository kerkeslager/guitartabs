from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
	path('register/', views.register, name='register'),
    path('<int:user_id>', views.profile, name='profile'),
]
