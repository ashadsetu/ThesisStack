from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ThesisUploadForm
from .models import Thesis
from django.contrib import messages
from django.shortcuts import render
from accounts.models import StudentProfile, ThesisGroup
from faculty.models import FacultyProfile, Supervision
from profiles.models import UserProfile

def home(request):
    context = {}
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
        context['profile'] = profile

        # student progress
        if request.user.role == 'student':
            group = ThesisGroup.objects.filter(members=request.user).first()
            supervision = Supervision.objects.filter(group=group).first()
            context['thesis_group'] = group
            context['supervision'] = supervision

        # faculty data
        elif request.user.role == 'supervisor':
            faculty = FacultyProfile.objects.filter(user=request.user).first()
            context['faculty'] = faculty

    return render(request, 'home.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')
        user = authenticate(request, username=username, password=password)

        if user:
            if user.role != selected_role:
                messages.error(request, "Role mismatch! Please select the correct role.")
                return redirect('login')

            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'supervisor':
                return redirect('faculty_dashboard')
            elif user.role == 'admin':
                return redirect('adm:admin_dashboard')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')
    return render(request, 'login.html')

def student_dashboard(request):
    theses = Thesis.objects.filter(student=request.user)
    return render(request, 'dashboard_student.html', {'theses': theses})

def supervisor_dashboard(request):
    theses = Thesis.objects.filter(supervisor=request.user)
    return render(request, 'faculty_dashboard.html', {'theses': theses})

def upload_thesis(request):
    if request.method == 'POST':
        form = ThesisUploadForm(request.POST, request.FILES)
        if form.is_valid():
            thesis = form.save(commit=False)
            thesis.student = request.user
            thesis.save()
            return redirect('student_dashboard')
    else:
        form = ThesisUploadForm()
    return render(request, 'upload_thesis.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')
