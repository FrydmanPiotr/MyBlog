from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404

from .models import Blog, Post, Author
from .forms import BlogForm, PostForm, AuthorForm

def index(request):
    """Strona główna aplikacji MyBlog."""
    return render(request, 'my_blog/index.html')

@login_required
def author(request):
    """Strona autora bloga."""
    author = Author.objects.filter(owner=request.user)
    context = {'author':author}
    return render(request, 'my_blog/author.html', context)

@login_required
def create_desc(request):
    """Utwórz opis o autorze."""
    if request.method != 'POST':
        # Nie zostały przekazane żadne dane. Utwórz pusty formularz.
        form = AuthorForm()
    else:
        # Przekazano dane za pomocą żądania POST. Przetwórz te dane.
        form = AuthorForm(data=request.POST)
        if form.is_valid():
            create_desc = form.save(commit=False)
            create_desc.owner = request.user
            create_desc.save()
            return redirect('my_blog:author')

    # Wyświetla pusty formularz.
    context = {'form': form}
    return render(request, 'my_blog/create_desc.html', context)

@login_required
def edit_desc(request):
    """Edycja opisu autora."""
    author = Author.objects.get(owner=request.user)
    if author.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Wypełnienie formularza aktualną treścią.
        form = AuthorForm(instance=author)
    else:
        # Przekazano dane za pomocą żądania POST. Przetwórz te dane.
        form = AuthorForm(instance=author, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_blog:author')

    context = {'author': author, 'form': form}
    return render(request, 'my_blog/edit_desc.html', context)

@login_required
def blogs(request):
    """Blogi użytkownika."""
    blogs = Blog.objects.filter(owner=request.user).order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'my_blog/blogs.html', context)

@login_required
def blog(request, blog_id):
    """Wyświetla blog użytkownika i opublikowane na nim posty."""
    blog = get_object_or_404(Blog, id=blog_id)
    """Sprawdzenie, czy blog należy do bieżącego użytkownika."""
    if blog.owner != request.user:
        raise Http404

    posts = blog.post_set.order_by('-date_added')
    context = {'blog': blog, 'posts': posts}
    return render(request, 'my_blog/blog.html', context)

@login_required
def new_blog(request):
    """Utwórz nowy blog."""
    if request.method != 'POST':
        # Nie zostały przekazane żadne dane. Utwórz pusty formularz.
        form = BlogForm()
    else:
        # Przekazano dane za pomocą żądania POST. Przetwórz te dane.
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect('my_blog:blogs')

    # Wyświetla pusty formularz.
    context = {'form': form}
    return render(request, 'my_blog/new_blog.html', context)

@login_required
def edit_blog_title(request, blog_id):
    """Edycja nazwy bloga."""
    blog = Blog.objects.get(id=blog_id)
    if blog.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Wypełnienie formularza aktualną treścią.
        form = BlogForm(instance=blog)
    else:
        # Przekazano dane za pomocą żądania POST. Przetwórz te dane.
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_blog:blog', blog.id)

    context = {'blog': blog, 'form': form}
    return render(request, 'my_blog/edit_blog_title.html', context)

@login_required
def delete_blog(request, blog_id):
    """Usuwanie bloga."""
    blog = Blog.objects.get(id=blog_id)
    # Sprawdzenie, czy bieżący użytkownik jest właścicielem bloga.
    if blog.owner != request.user:
        raise Http404

    if blog.owner.id == request.user.id:
        if request.method == 'POST':
            blog.delete()
            return redirect('my_blog:blogs')

    context = {'blog': blog}
    return render(request, 'my_blog/delete_blog.html', context)

@login_required
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

@login_required
def edit_post(request, post_id):
    """Edycja istniejącego postu."""
    post = Post.objects.get(id=post_id)
    blog = post.blog
    # Sprawdzenie, czy bieżący użytkownik jest właścicielem bloga.
    if blog.owner != request.user:
        raise Http404

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

@login_required
def delete_post(request, post_id):
    "Usuwanie istniejącego postu."
    post = Post.objects.get(id=post_id)
    blog = post.blog
    # Sprawdzenie, czy bieżący użytkownik jest właścicielem bloga.
    if blog.owner != request.user:
        raise Http404

    if blog.owner.id == request.user.id:
        if request.method == 'POST':
            post.delete()
            return redirect('my_blog:blog', blog.id)

    context = {'post': post, 'blog': blog}
    return render(request, 'my_blog/delete_post.html', context)
