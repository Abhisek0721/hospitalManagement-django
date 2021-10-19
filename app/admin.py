from django.contrib import admin
from .models import SignupDoctor, SignupPatient, CreateBlog

# Register your models here.
admin.site.register(SignupDoctor)
admin.site.register(SignupPatient)
admin.site.register(CreateBlog)