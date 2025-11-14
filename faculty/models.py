from django.db import models
from django.conf import settings
from accounts.models import ThesisGroup


class FacultyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    seniority_rank = models.PositiveIntegerField(help_text="1 = most senior, higher number = junior")
    department = models.CharField(max_length=100, default="CSE")

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.designation})"


class Supervision(models.Model):
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'supervisor'}
    )
    group = models.OneToOneField('accounts.ThesisGroup', on_delete=models.CASCADE)
    round_assigned = models.PositiveIntegerField(default=1)
    selected_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.group.name} supervised by {self.supervisor} ({self.status})"


class Communication(models.Model):
    supervision = models.ForeignKey(Supervision, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}"


class FacultyFeedback(models.Model):
    supervision = models.ForeignKey(Supervision, on_delete=models.CASCADE, related_name='feedbacks')
    comments = models.TextField()
    file = models.FileField(upload_to='faculty_feedback/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.supervision.supervisor} on {self.supervision.group.name}"
