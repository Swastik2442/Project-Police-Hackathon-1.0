from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_view(request: HttpRequest):
    """The Django View for the Website Login Page."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next", "siteIndex"))
        else:
            return render(request, 'base/login.html', {'error': True})
    else:
        return render(request, 'base/login.html')

def logout_view(request: HttpRequest):
    """The Django View for the Website Logout Page."""
    logout(request)
    return redirect(request.GET.get("next", "siteIndex"))

def signup_view(request: HttpRequest):
    """The Django View for the Website Sign-Up Page."""
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        # TODO: Can be improved with multiple types of error codes
        try:
            newUser = User(username=phone, password=password, first_name=firstname, last_name=lastname, email=email)
            newUser.save()
        except Exception:
            return render(request, 'base/signup.html', {'error': True})
    else:
        return render(request, 'base/signup.html')

def index_view(request: HttpRequest):
    """The Django View for the Website Home Page."""
    return render(request, 'base/index.html')