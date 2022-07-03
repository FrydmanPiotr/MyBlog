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
    # Strona przeznaczona do utworzenia nowego bloga.
    path('new_blog/', views.new_blog, name='new_blog'),
    # Strona przeznaczona do edycji nazwy bloga.
    path('edit_blog_title/<int:blog_id>/', views.edit_blog_title, name='edit_blog_title'),
    # Strona przeznaczona do utworzenia nowego postu.
    path('new_post/(<int:blog_id>)/', views.new_post, name='new_post'),
    # Strona przeznaczona do edycji postu.
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
]
