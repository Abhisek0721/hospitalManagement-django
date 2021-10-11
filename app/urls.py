from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signupDoctor/", views.signupDoctor, name="signupDoctor"),
    path("signupPatient/", views.signupPatient, name="signupPatient"),
    path("loginDoctor/", views.loginDoctor, name="loginDoctor"),
    path("loginPatient/", views.loginPatient, name="loginPatient"),
    path("doctorDashboard/", views.doctorDashboard, name="doctorDashboard"),
    path("patientDashboard/", views.patientDashboard, name="patientDashboard"),
    path("logout/", views.logout, name="logout"),
]