from django.db import models
from django.conf import settings


class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, default='CSE')
    designation = models.CharField(max_length=100, default='Department Admin')
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.department})"
