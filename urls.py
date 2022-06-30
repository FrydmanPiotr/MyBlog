"""Definiuje wzorce adresów URL dla aplikacji my_blog."""

from django.urls import path

from . import views

app_name = 'my_blog'
urlpatterns = [
    # Strona główna.
    path('', views.home, name='home'),
    # Blogi utworzone przez użytkownika.
    path('blogs/', views.blogs, name='blogs'),
    # Strona bloga użytkownika.
    path('blogs/(<int:blog_id>)/', views.blog, name='blog'),
]
