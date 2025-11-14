from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Thesis, Feedback

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'role', 'password1', 'password2']


class ThesisUploadForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ['title', 'description']

