from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ThesisGroup, ThesisSubmission, StudentProfile
from .forms import ThesisGroupForm, ThesisSubmissionForm, StudentLoginForm , StudentProfileForm
from faculty.models import Supervision
from main.models import Feedback

def student_login(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('student_dashboard')
        elif request.user.role == 'supervisor':
            return redirect('faculty_dashboard')
    if request.method == "POST":
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'supervisor':
                return redirect('faculty_dashboard')
            else:
                messages.error(request, "Invalid role. Contact admin.")
                return redirect('student_login')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = StudentLoginForm()
    return render(request, 'login.html', {'form': form})

def student_logout(request):
    logout(request)
    return redirect('home')

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('home')

    profile = StudentProfile.objects.filter(user=request.user).first()
    user_profile = None
    from profiles.models import UserProfile
    user_profile = UserProfile.objects.filter(user=request.user).first()

    groups = ThesisGroup.objects.filter(members=request.user) | ThesisGroup.objects.filter(creator=request.user)
    groups = groups.distinct()
    submissions = ThesisSubmission.objects.filter(student=request.user)


    return render(request, 'dashboard.html', {
        'profile': profile,
        'user_profile': user_profile,
        'groups': groups,

    })

@login_required
def create_group(request):
    if request.user.role != 'student':
        return redirect('login')
    if request.method == 'POST':
        form = ThesisGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            form.save_m2m()
            group.members.add(request.user)
            return redirect('student_dashboard')
    else:
        form = ThesisGroupForm()
    return render(request, 'create_group.html', {'form': form})


@login_required
def upload_thesis(request):
    if request.method == 'POST':
        form = ThesisSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            thesis = form.save(commit=False)
            thesis.student = request.user
            group = ThesisGroup.objects.filter(members=request.user).first()
            thesis.group = group
            thesis.save()
            messages.success(request, "Thesis uploaded successfully!")
            return redirect('student_dashboard')
    else:
        form = ThesisSubmissionForm()
    return render(request, 'upload_thesis.html', {'form': form})

@login_required
def view_feedback(request):
    group = ThesisGroup.objects.filter(members=request.user).first()
    supervision = Supervision.objects.filter(group=group).first()
    status_message = None
    if supervision:
        if supervision.status == 'accepted':
            status_message = "Your thesis group has been accepted by faculty."
        elif supervision.status == 'rejected':
            status_message = "Your thesis group was not accepted by faculty."
        else:
            status_message = "Awaiting faculty response."
    feedbacks = Feedback.objects.filter(thesis__student=request.user)
    return render(request, 'view_feedback.html', {'feedbacks': feedbacks, 'status_message': status_message})

@login_required
def profile_edit(request):
    from .forms import StudentProfileForm
    from .models import StudentProfile

    profile, _ = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})

@login_required
def created_groups(request):
    if request.user.role != 'student':

        return redirect('home')

    groups = ThesisGroup.objects.filter(creator=request.user)

    group_data = []
    for g in groups:
        submissions = ThesisSubmission.objects.filter(group=g)

        feedbacks = Feedback.objects.filter(thesis__in=submissions.values_list('id', flat=True))

        total_steps = 10
        done = 0
        if g:
            done += 1
        if submissions.exists():
            done += 1
        if feedbacks.exists():
            done += 1
        progress = int((done / total_steps) * 100)

        group_data.append({
            'group': g,
            'progress': progress,
            'members': g.members.all(),
            'submissions': submissions,
            'feedback_count': feedbacks.count(),
        })

    return render(request, 'created_group.html', {'group_data': group_data})


def delete_group(request , group_id):
    group = get_object_or_404(ThesisGroup, id=group_id)

    if group.creator != request.user:
        messages.error(request, "You are not authorized to delete this group.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        ThesisSubmission.objects.filter(group=group).delete()
        Supervision.objects.filter(group=group).delete()
        group.delete()

        messages.success(request, f"Group '{group.name}' deleted successfully!")
        return redirect('student_dashboard')

    return render(request, 'delete_group.html', {'group': group})
