from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("company", "Company"),
        ("tpo", "TPO"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    roll_number = models.CharField(max_length=50, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    graduation_year = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

from django.contrib.auth.hashers import make_password, check_password

class UserAccount(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('company', 'Company'),
        ('tpo', 'TPO'),
    ]
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # hashed password
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.full_name} ({self.role})"