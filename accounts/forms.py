from django import forms
from .models import ThesisGroup, ThesisSubmission, StudentProfile


class StudentLoginForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@uap-bd.edu'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class ThesisGroupForm(forms.ModelForm):
    class Meta:
        model = ThesisGroup
        fields = ['name', 'topic', 'members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Name'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thesis Topic'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        students = StudentProfile.objects.select_related('user').order_by('-cgpa')
        choices = []
        for student in students:
            full_name = f"{student.user.first_name} {student.user.last_name}".strip() or student.user.username
            label = f"{full_name} ({student.cgpa})"
            choices.append((student.user.id, label))
        self.fields['members'].choices = choices

class ThesisSubmissionForm(forms.ModelForm):
    class Meta:
        model = ThesisSubmission
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Thesis Title'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['batch', 'cgpa', 'image']
        widgets = {
            'batch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Batch'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

