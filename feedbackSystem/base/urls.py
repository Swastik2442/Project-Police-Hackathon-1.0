from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="siteIndex"),
    path("login/", views.login_view, name="siteLogin"),
    path("signup/", views.signup_view, name="siteSignup"),
    path("logout/", views.logout_view, name="siteLogout"),
    path("verify/<str:uid>", views.verify_view, name="siteVerify"),
    path("resend/<str:uid>", views.resendOTP_view, name="siteOTPResend"),
]