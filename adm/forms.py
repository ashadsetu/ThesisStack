from django import forms
from accounts.models import StudentProfile
from faculty.models import FacultyProfile
from main.models import User


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class StudentProfileAdminForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['reg_id', 'batch', 'cgpa']
        widgets = {
            'reg_id': forms.TextInput(attrs={'class': 'form-control'}),
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class FacultyProfileAdminForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = ['designation', 'department', 'seniority_rank']
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'seniority_rank': forms.NumberInput(attrs={'class': 'form-control'}),
        }
