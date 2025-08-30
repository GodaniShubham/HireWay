from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    package = models.CharField(max_length=20)  # e.g., '6-8 LPA'
    eligibility = models.CharField(max_length=100)
    domain = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} - {self.company}"

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('offer_received', 'Offer Received'),
    ])

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"