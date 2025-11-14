from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from accounts.models import ThesisSubmission

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"


class Thesis(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='theses',
        limit_choices_to={'role': 'student'}
    )
    supervisor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='supervised_theses', limit_choices_to={'role': 'supervisor'}
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    thesis = models.ForeignKey(ThesisSubmission, on_delete=models.CASCADE, related_name='feedbacks')
    supervisor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='given_feedbacks',
        limit_choices_to={'role': 'supervisor'}
    )
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.supervisor} on {self.thesis.title}"
