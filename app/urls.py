from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("signupDoctor/", views.signupDoctor, name="signupDoctor"),
    path("signupPatient/", views.signupPatient, name="signupPatient"),
    path("loginDoctor/", views.loginDoctor, name="loginDoctor"),
    path("loginPatient/", views.loginPatient, name="loginPatient"),
    path("doctorDashboard/", views.doctorDashboard, name="doctorDashboard"),
    path("patientDashboard/", views.patientDashboard, name="patientDashboard"),
    path("logout/", views.logout, name="logout"),
    path("createblog/", views.createBlogs, name="createBlogs"),
    path("viewblog/", views.viewBlogs, name="viewBlogs"),
    path("draft/", views.draft, name="draft"),
]


urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)