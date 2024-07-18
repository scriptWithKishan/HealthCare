from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, PrescriptionForm, ReportForm
from .models import Prescription, Report, CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_patient:
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'medical/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_patient:
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
    return render(request, 'medical/login.html')

@login_required
def patient_dashboard(request):
    prescriptions = Prescription.objects.filter(patient__user=request.user)
    reports = Report.objects.filter(patient__user=request.user)
    return render(request, 'medical/patient_dashboard.html', {'prescriptions': prescriptions, 'reports': reports})

@login_required
def doctor_dashboard(request):
    patients = CustomUser.objects.filter(is_patient=True)
    return render(request, 'medical/doctor_dashboard.html', {'patients': patients})

@login_required
def add_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user.doctor
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()
    return render(request, 'medical/add_prescription.html', {'form': form})

@login_required
def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.doctor = request.user.doctor
            report.save()
            return redirect('doctor_dashboard')
    else:
        form = ReportForm()
    return render(request, 'medical/add_report.html', {'form': form})
