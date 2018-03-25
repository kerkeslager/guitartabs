from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('contact/', include('contact.urls')),
    path('tabs/', include('tabs.urls')),
    path('users/', include('users.urls')),

    path('auth/login/', auth_views.login, name='login'),
    path('auth/logout/', auth_views.logout, name='logout'),
    path('auth/register/', views.register, name='register'),
    path('auth/request_reset/', auth_views.password_reset, name='password_reset'),
    path('auth/request_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    re_path(r'auth/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('auth/reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
]
