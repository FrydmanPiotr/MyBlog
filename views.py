from django.shortcuts import render

from .models import Blog

def home(request):
    """Strona główna aplikacji MyBlog."""
    return render(request, 'my_blog/home.html')

def blogs(request):
    """Blogi użytkownika."""
    blogs = Blog.objects.order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'my_blog/blogs.html', context)

def blog(request, blog_id):
    """Wyświetla blog użytkownika i opublikowane na nim posty."""
    blog = Blog.objects.get(id=blog_id)
    posts = blog.post_set.order_by('-date_added')
    context = {'blog': blog, 'posts': posts}
    return render(request, 'my_blog/blog.html', context)
    