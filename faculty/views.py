from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import User
from accounts.models import ThesisGroup, ThesisSubmission
from .models import FacultyProfile, Supervision
from .forms import FacultyLoginForm

def faculty_login(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    if request.user.is_authenticated and request.user.role == 'supervisor':
        return redirect('faculty_dashboard')

    if request.method == "POST":
        form = FacultyLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role != 'supervisor':
                messages.error(request, "Access denied. Only faculty can log in here.")
                return redirect('faculty_login')

            login(request, user)
            return redirect('faculty_dashboard')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = FacultyLoginForm()

    return render(request, 'faculty/login.html', {'form': form})

def faculty_logout(request):
    logout(request)
    return redirect('home')

@login_required
def faculty_dashboard(request):
    if request.user.role != 'supervisor':
        messages.error(request, "Access denied.")
        return redirect('login')

    faculty, _ = FacultyProfile.objects.get_or_create(
        user=request.user,
        defaults={'designation': 'Lecturer', 'seniority_rank': 99, 'department': 'CSE'}
    )

    my_groups = ThesisGroup.objects.filter(supervision__supervisor=request.user)
    unassigned_groups = ThesisGroup.objects.filter(supervision__isnull=True)

    groups = list(unassigned_groups)
    groups.sort(key=lambda g: g.group_cgpa, reverse=True)

    return render(request, 'faculty/faculty_dashboard.html', {
        'faculty': faculty,
        'groups': groups,
        'my_groups': my_groups
    })


@login_required
def group_detail(request, group_id):
    if request.user.role != 'supervisor':
        return redirect('faculty_dashboard')

    group = get_object_or_404(ThesisGroup, id=group_id)
    return render(request, 'faculty/group_detail.html', {'group': group})


@login_required
def select_group(request, group_id):
    if request.user.role != 'supervisor':
        messages.error(request, "Access denied.")
        return redirect('faculty_dashboard')

    faculty, _ = FacultyProfile.objects.get_or_create(
        user=request.user,
        defaults={'designation': 'Lecturer', 'seniority_rank': 99, 'department': 'CSE'}
    )

    seniors_pending = FacultyProfile.objects.filter(seniority_rank__lt=faculty.seniority_rank)
    seniors_unselected = [
        f for f in seniors_pending if not Supervision.objects.filter(supervisor=f.user).exists()
    ]

    if seniors_unselected:
        messages.warning(
            request,
            f"Senior faculty ({seniors_unselected[0].user.get_full_name()}) must choose first."
        )
        return redirect('faculty_dashboard')

    group = get_object_or_404(ThesisGroup, id=group_id)
    if Supervision.objects.filter(group=group).exists():
        messages.error(request, "This group is already assigned.")
        return redirect('faculty_dashboard')

    Supervision.objects.create(supervisor=request.user, group=group, status='accepted')
    messages.success(request, f"You are now supervising '{group.name}'.")
    return redirect('faculty_dashboard')


@login_required
def accept_group(request, group_id):
    if request.user.role != 'supervisor':
        return redirect('faculty_dashboard')

    group = get_object_or_404(ThesisGroup, id=group_id)
    supervision, created = Supervision.objects.get_or_create(
        supervisor=request.user, group=group, defaults={'status': 'accepted'}
    )
    if not created:
        supervision.status = 'accepted'
        supervision.save()

    messages.success(request, f"You have accepted '{group.name}'.")
    return redirect('faculty_dashboard')


@login_required
def reject_group(request, group_id):
    if request.user.role != 'supervisor':
        return redirect('faculty_dashboard')

    group = get_object_or_404(ThesisGroup, id=group_id)
    supervision = Supervision.objects.filter(group=group, supervisor=request.user).first()

    if supervision:
        supervision.delete()
        messages.info(request, f"The group '{group.name}' has been removed from your supervision.")
    else:
        messages.warning(request, f"No supervision found for '{group.name}'.")

    return redirect('faculty_dashboard')


@login_required
def delete_group(request, group_id):
    if request.user.role != 'supervisor':
        messages.error(request, "Access denied.")
        return redirect('faculty_dashboard')

    group = get_object_or_404(ThesisGroup, id=group_id)

    if request.method == 'POST':
        Supervision.objects.filter(group=group).delete()
        group.delete()
        messages.success(request, f"The group '{group.name}' has been deleted from the system.")
        return redirect('faculty_dashboard')

    return render(request, 'faculty/delete_group.html', {'group': group})


@login_required
def view_submissions(request, group_id):
    if request.user.role != 'supervisor':
        messages.error(request, "Access denied.")
        return redirect('student_dashboard')

    group = get_object_or_404(ThesisGroup, id=group_id)
    submissions = ThesisSubmission.objects.filter(group=group)

    if request.method == "POST":
        thesis_id = request.POST.get("thesis_id")
        comment = request.POST.get("comment")

        if thesis_id and comment:
            thesis = get_object_or_404(ThesisSubmission, id=thesis_id)
            Feedback.objects.create(
                thesis=thesis,
                supervisor=request.user,
                comments=comment
            )
            messages.success(request, f"Feedback added for {thesis.title}.")
            return redirect('view_submissions', group_id=group.id)
        else:
            messages.error(request, "Please select a thesis and write a comment before submitting.")

    return render(request, 'faculty/view_submissions.html', {
        'group': group,
        'submissions': submissions
    })

