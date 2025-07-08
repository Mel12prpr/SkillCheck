from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('registration_success')
        else:
            return render(request, 'User/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'User/register.html', {'form': form})

def registration_success(request):
    return render(request, 'User/registration_success.html')




def user_login(request):
    error_message = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password"

    return render(request, 'User/login.html', {'error_message': error_message})


def user_logout(request):
    logout(request)
    return redirect('login')
