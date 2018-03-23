from django.urls import path

from . import views

app_name = 'tabs'
urlpatterns = [
    path('', views.index, name='index'),
    path('instrument/<str:instrument>/', views.instrument, name='instrument'),
    path('<int:tab_id>/edit/', views.edit, name='edit'),
    path('<int:tab_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
]
