from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from accounts.models import ThesisGroup
from faculty.models import Supervision

@login_required
def view_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    selection_notice = None
    if request.user.role == 'student':
        group = ThesisGroup.objects.filter(members=request.user).first()
        if group:
            sup = Supervision.objects.filter(group=group).select_related('supervisor').first()
            if sup:
                selection_notice = f"{sup.supervisor.get_full_name() or sup.supervisor.username} selected your group."
    return render(request, 'profiles/view_profile.html', {'profile': profile, 'selection_notice': selection_notice})

@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profiles:view_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})


def delete_profile():
    return None