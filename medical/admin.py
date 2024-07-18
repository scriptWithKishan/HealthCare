from django.contrib import admin
from .models import CustomUser, Patient, Doctor, Prescription, Report

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Prescription)
admin.site.register(Report)