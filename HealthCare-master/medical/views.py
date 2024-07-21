from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Prescription, Report, CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect


CustomUser = get_user_model()

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        is_patient = request.POST.get('is_patient', 'off') == 'on'

        if password1 == password2:
            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password1),
                is_patient=is_patient
            )
            user.save()
            if user.is_patient:
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
        else:
            error = "Passwords do not match"
            return render(request, 'medical/register.html', {'error': error})

    return render(request, 'medical/register.html')

def login_view(request):
    message = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            message = ""
            login(request, user)
            if user.is_patient:
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
        else:
            message = "user does not exist"
    else: 
        message = ""
    return render(request, 'medical/login.html', {
        'message': message
    })

@login_required
def patient_dashboard(request):
    prescriptions = Prescription.objects.filter(patient__user=request.user)
    reports = Report.objects.filter(patient__user=request.user)

    if request.method == "POST":
        logout(request)
        return redirect('login')
    return render(request, 'medical/patient_dashboard.html', {'prescriptions': prescriptions, 'reports': reports})

@login_required
def doctor_dashboard(request):
    patients = CustomUser.objects.filter(is_patient=True)

    if request.method == "POST":
        logout(request)
        return redirect('login')
    return render(request, 'medical/doctor_dashboard.html', {'patients': patients})

@login_required
def add_prescription(request):
    if request.method == 'POST':
        patient = request.POST['patient']
        medication = request.POST['medication']
        dosage = request.POST['dosage']
        instructions = request.POST['instructions']

        prescription = Prescription(
            doctor=request.user.doctor,
            patient=patient,
            medication=medication,
            dosage=dosage,
            instructions=instructions
        )
        prescription.save()
        return redirect('doctor_dashboard')

    return render(request, 'medical/add_prescription.html')

@login_required
def add_report(request):
    if request.method == 'POST':
        patient = request.POST['patient']
        report_type = request.POST['report_type']
        description = request.POST['description']

        report = Report(
            doctor=request.user.doctor,
            patient=patient,
            report_type=report_type,
            description=description
        )
        report.save()
        return redirect('doctor_dashboard')

    return render(request, 'medical/add_report.html')