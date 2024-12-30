from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parsed_content = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, blank=True)
    file_size = models.IntegerField(default=0)  # Size in KB

    def save(self, *args, **kwargs):
        if self.file:
            self.file_type = self.file.name.split('.')[-1].lower()
            self.file_size = self.file.size // 1024
        super().save(*args, **kwargs)

class CareerAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    target_field = models.CharField(max_length=255)
    transferable_skills = models.JSONField()
    suggested_activities = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)
    skill_categories = models.JSONField(default=dict)  # For analytics

    class Meta:
        ordering = ['-created_at']
