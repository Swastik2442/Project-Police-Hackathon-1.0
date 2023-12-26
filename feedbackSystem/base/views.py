from random import randint

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseBadRequest
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test

from .models import Profile
from .utils import initialSetup
from .messaging import MessageHandler
from feedbackSystem.settings import LANGUAGE_CODE, COUNTRY_E146_CODE

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
            newUser = User.objects.create(username=phone, first_name=firstName, last_name=lastName, email=email)
            newUser.set_password(password1)
            newUser.save()

            nvGroup = Group.objects.get(name='authNotVerified')
            newUser.groups.add(nvGroup)

            user = authenticate(request, username=phone, password=password1)
            if user is None:
                raise ValueError()
            else:
                login(request, user)

            otp = str(randint(1000, 9999))
            profile = Profile.objects.create(user=user, phone=phone, otp=otp)
            MessageHandler(phone, otp).sendOTP(request.COOKIES.get('django_language', LANGUAGE_CODE))

            response = redirect("siteVerify", profile.uid)
            response.set_cookie("can_otp_enter", True, max_age=600)
            return response
        except Exception:
            return render(request, 'base/signup.html', {'error': True})
    return render(request, 'base/signup.html')

def isNotVerifiedUser(user):
    """Checks if Current User is not Verified."""
    return user.groups.filter(name='authNotVerified').exists()

@user_passes_test(isNotVerifiedUser, '/login')
def resendOTP_view(request: HttpRequest, uid: str):
    """A Django View for Resending OTP according to the provided UID."""
    try:
        profile = Profile.objects.get(uid=uid)
        MessageHandler(profile.phone, profile.otp).sendOTP(request.COOKIES.get('django_language', LANGUAGE_CODE))
        response = redirect("siteVerify", profile.uid)
        response.set_cookie("can_otp_enter", True, max_age=600)
        return response
    except Exception:
        raise HttpResponseBadRequest('No Such UID found')

@user_passes_test(isNotVerifiedUser, '/login')
def verify_view(request: HttpRequest, uid: str):
    """A Django View for the OTP Verification Page."""
    profile = Profile.objects.get(uid=uid)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if profile.otp == otp:
            profile.delete()
            nvGroup = Group.objects.get(name='authNotVerified')
            vGroup = Group.objects.get(name='authVerified')
            request.user.groups.remove(nvGroup)
            request.user.groups.add(vGroup)
            return redirect(request.GET.get("next", "siteIndex"))
        return render(request, 'base/verify.html', {'countryCode': COUNTRY_E146_CODE, 'phone': profile.phone, 'error': True})
    return render(request, 'base/verify.html', {'countryCode': COUNTRY_E146_CODE, 'phone': profile.phone})

def index_view(request: HttpRequest):
    """A Django View for the Website Home Page."""
    return render(request, 'base/index.html')