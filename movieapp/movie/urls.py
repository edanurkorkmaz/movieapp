from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_film/', views.add_film, name='add_film'),
    path('favori_film/', views.favori_film, name='favori_film'),
    path('film/<int:film_id>/', views.film_detay, name='film_detay'),

   ]

