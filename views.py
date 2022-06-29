from django.shortcuts import render

def home(request):
    """Strona główna aplikacji MyBlog."""
    return render(request, 'my_blog/home.html')