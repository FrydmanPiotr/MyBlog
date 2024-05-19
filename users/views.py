from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Rejestracja nowego użytkownika."""
    if request.method != 'POST':
        # Wyświetla pusty formularz rejestracji użytkownika.
        form = UserCreationForm()
    else:
        # Przetwarza wypełniony formularz.
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Zalogowanie użytkownika i przekierowanie go na stronę główną.
            login(request, new_user)
            return redirect('my_blog:index')

    # Wyświetla pusty formularz.
    context = {'form': form}
    return render(request, 'registration/register.html', context)
