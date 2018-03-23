from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tabs/', include('tabs.urls')),
    path('users/', include('users.urls')),

	path(r'users/request_password_reset/', auth_views.password_reset, name='password_reset'),
    path(r'users/request_password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    path(r'users/reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path(r'users/reset_password/done/', auth_views.password_reset_complete, name='password_reset_complete'),
]
