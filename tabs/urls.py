from django.urls import path

from . import views

app_name = 'tabs'
urlpatterns = [
    path('', views.index, name='index'),
    path('artists/create/', views.artist_create, name='artist_create'),
    path('artists/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('artists/', views.artist_index, name='artist_index'),
    path('example/', views.example, name='example'),
    path('instrument/<str:instrument>/', views.instrument, name='instrument'),
    path('<int:tab_id>/edit/', views.edit, name='edit'),
    path('<int:tab_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
]
