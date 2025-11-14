from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import FacultyProfile


class FacultyLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Faculty Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "example@uap-bd.edu",
        })
    )

    def clean_username(self):
        email = self.cleaned_data.get("username")
        if not email.endswith("@uap-bd.edu"):
            raise ValidationError("Please use your official @uap-bd.edu email address.")
        return email
class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = ['designation', 'seniority_rank', 'department']
        widgets = {
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Designation (e.g. Professor, Lecturer)'
            }),
            'seniority_rank': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter Seniority Rank (1 = most senior)'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Department (e.g. CSE)'
            }),
        }