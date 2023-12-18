from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_view(request: HttpRequest):
    """A Django View for the Website Login Page."""
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(request, username=phone, password=password)
        if user is None:
            return render(request, 'base/login.html', {'error': True})
        login(request, user)
        return redirect(request.GET.get("next", "siteIndex"))
    else:
        return render(request, 'base/login.html')

def logout_view(request: HttpRequest):
    """A Django View for the Website Logout Page."""
    logout(request)
    return redirect(request.GET.get("next", "siteIndex"))

# TODO: Add OTP Method
def signup_view(request: HttpRequest):
    """A Django View for the Website Sign-Up Page."""
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName', '')
        email = request.POST.get('email', '')
        phone = str(request.POST.get('phone'))
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2: return render(request, 'base/signup.html', {'error': True})
        try:
            newUser = User(username=phone, first_name=firstName, last_name=lastName, email=email)
            newUser.set_password(password1)
            newUser.save()
            return redirect(request.GET.get("next", "siteIndex"))
        except Exception:
            return render(request, 'base/signup.html', {'error': True})
    else:
        return render(request, 'base/signup.html')

def index_view(request: HttpRequest):
    """A Django View for the Website Home Page."""
    return render(request, 'base/index.html')