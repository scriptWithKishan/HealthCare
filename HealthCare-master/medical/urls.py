from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('add_prescription/', views.add_prescription, name='add_prescription'),
    path('add_report/', views.add_report, name='add_report'),
]