from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Prescription, Report


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'is_patient', 'is_doctor')

    def clean(self):
        cleaned_data = super().clean()
        is_patient = cleaned_data.get('is_patient')
        is_doctor = cleaned_data.get('is_doctor')

        if is_patient and is_doctor:
            raise forms.ValidationError("You can only select either Patient or Doctor, not both.")
        if not is_patient and not is_doctor:
            raise forms.ValidationError("You must select either Patient or Doctor.")
        
        return cleaned_data

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medication', 'dosage', 'frequency', 'start_date', 'end_date', 'notes']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['patient', 'report_date', 'diagnosis', 'treatment', 'notes']
