from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect
from .models import Prescription, Report, CustomUser, Patient, Doctor
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        is_patient = request.POST.get('is_patient', 'off') == 'on'
        is_doctor = request.POST.get('is_doctor', 'off') == 'on'

        if password1 == password2:
            if is_patient and is_doctor:
                error = "You can only select either Patient or Doctor, not both."
                return render(request, 'medical/register.html', {'error': error})
            if not is_patient and not is_doctor:
                error = "You must select either Patient or Doctor."
                return render(request, 'medical/register.html', {'error': error})

            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password1),
                is_patient=is_patient,
                is_doctor=is_doctor
            )
            user.save()

            if is_patient:
                Patient.objects.create(user=user)
                return redirect('patient_dashboard')
            elif is_doctor:
                Doctor.objects.create(user=user)
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
    try:
        patient = Patient.objects.get(user=request.user)
        prescriptions = Prescription.objects.filter(patient=patient)
        reports = Report.objects.filter(patient=patient)
    except Patient.DoesNotExist:
        prescriptions = []
        reports = []

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
    patients = Patient.objects.all()
    if request.method == 'POST':
        patient_id = request.POST['patient']
        medication = request.POST['medication']
        dosage = request.POST['dosage']
        frequency = request.POST['frequency']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        notes = request.POST['notes']

        try:
            patient = Patient.objects.get(pk=patient_id)
            doctor = Doctor.objects.get(user=request.user)
            prescription = Prescription(
                patient=patient,
                doctor=doctor,
                medication=medication,
                dosage=dosage,
                frequency=frequency,
                start_date=start_date,
                end_date=end_date,
                notes=notes
            )
            prescription.save()
            return redirect('doctor_dashboard')
        except Patient.DoesNotExist:
            error = "Patient does not exist."
            return render(request, 'medical/add_prescription.html', {'error': error, 'patients': patients})

    return render(request, 'medical/add_prescription.html', {'patients': patients})

@login_required
def add_report(request):
    patients = Patient.objects.all()
    if request.method == 'POST':
        patient_id = request.POST['patient']
        report_date = request.POST['report_date']
        diagnosis = request.POST['diagnosis']
        treatment = request.POST['treatment']
        notes = request.POST['notes']

        try:
            patient = Patient.objects.get(pk=patient_id)
            doctor = Doctor.objects.get(user=request.user)
            report = Report(
                patient=patient,
                doctor=doctor,
                report_date=report_date,
                diagnosis=diagnosis,
                treatment=treatment,
                notes=notes
            )
            report.save()
            return redirect('doctor_dashboard')
        except Patient.DoesNotExist:
            error = "Patient does not exist."
            return render(request, 'medical/add_report.html', {'error': error, 'patients': patients})

    return render(request, 'medical/add_report.html', {'patients': patients})
