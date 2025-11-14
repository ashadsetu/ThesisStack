from django.db import models
from django.conf import settings
from decimal import Decimal
from django.db.models import Avg

def upload_to_thesis(instance, filename):
    return f"thesis_files/{instance.student.username}/{filename}"

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reg_id = models.CharField(max_length=20, unique=True)
    batch = models.CharField(max_length=10)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='profile_pics/', default='default_profile.jpg')
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.reg_id})"


class ThesisGroup(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.topic}"

    @property
    def group_cgpa(self):
        profiles = StudentProfile.objects.filter(user__in=self.members.all())
        if profiles.exists():
            avg_cgpa = profiles.aggregate(Avg('cgpa'))['cgpa__avg'] or Decimal('0.00')
            return round(avg_cgpa, 2)
        return Decimal('0.00')

    def is_member(self, user):
        return user == self.creator or user in self.members.all()

class ThesisSubmission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(ThesisGroup, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=upload_to_thesis)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.student.get_full_name()}"
