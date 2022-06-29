"""Definiuje wzorce adresów URL dla aplikacji my_blog."""

from django.urls import path

from . import views

app_name = 'my_blog'
urlpatterns = [
    # Strona główna.
    path('', views.home, name='home'),
]
