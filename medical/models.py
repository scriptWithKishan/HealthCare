from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255, default='General')


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField()

class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    report_date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField()
