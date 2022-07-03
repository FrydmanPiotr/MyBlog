from django.shortcuts import render, redirect

from .models import Blog, Post
from .forms import BlogForm, PostForm

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

def new_blog(request):
    """Utwórz nowy blog."""
    if request.method != 'POST':
        # Nie zostały przekazane żadne dane. Utwórz pusty formularz.
        form = BlogForm()
    else:
        # Przekazano dane za pomocą żądania POST. Przetwórz te dane.
        form = BlogForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_blog:blogs')

    # Wyświetla pusty formularz.
    context = {'form': form}
    return render(request, 'my_blog/new_blog.html', context)

def new_post(request, blog_id):
    """Tworzenie nowego postu na blogu."""
    blog = Blog.objects.get(id=blog_id)

    if request.method != 'POST':
        # Nie zostały przekazane żadne dane. Utwórz pusty formularz.
        form = PostForm()
    else:
        # Przekazano dane za pomocą żądania POST. Przetwórz te dane.
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect('my_blog:blog', blog_id=blog_id)

    # Wyświetla pusty formularz.
    context = {'blog': blog, 'form': form}
    return render(request, 'my_blog/new_post.html', context)

def edit_post(request, post_id):
    """Edycja istniejącego postu."""
    post = Post.objects.get(id=post_id)
    blog = post.blog

    if request.method != 'POST':
        # Wypełnienie formularza aktualną treścią.
        form = PostForm(instance=post)
    else:
        # Przekazano dane za pomocą żądania POST. Przetwórz te dane.
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_blog:blog', blog.id)

    context = {'post': post, 'blog': blog, 'form': form}
    return render(request, 'my_blog/edit_post.html', context)

def edit_blog_title(request, blog_id):
    """Edycja nazwy bloga."""
    blog = Blog.objects.get(id=blog_id)

    if request.method != 'POST':
        # Wypełnienie formularza aktualną treścią.
        form = BlogForm(instance=blog)
    else:
        # Przekazano dane za pomocą żądania POST. Przetwórz te dane.
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_blog:blogs')

    context = {'blog': blog, 'form': form}
    return render(request, 'my_blog/edit_blog.html', context)