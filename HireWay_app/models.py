from django.db import models
from django.contrib.auth.models import User


# 🔹 Student Profile
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    applied_jobs_count = models.IntegerField(default=0)
    upcoming_exams_count = models.IntegerField(default=0)
    placement_status = models.CharField(
        max_length=50,
        choices=[("Not Placed", "Not Placed"), ("Placed", "Placed")],
        default="Not Placed"
    )

    def __str__(self):
        return self.user.username


# 🔹 Notifications for Students
class Notification(models.Model):
    student = models.ForeignKey(Student, related_name="notifications", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)  # DateTime for exact timestamp

    def __str__(self):
        return f"{self.student.user.username} - {self.message[:30]}"


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=50, choices=[
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('offer_received', 'Offer Received'),
    ], default="applied")

    def __str__(self):
        return f"{self.user.username} - {self.job.title} ({self.status})"



class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_profile")
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

    # 🔹 Dynamic properties (instead of storing static counts)
    @property
    def total_jobs(self):
        return Job.objects.filter(company=self.name).count()

    @property
    def applicants_received(self):
        return Application.objects.filter(job__company=self.name).count()

    @property
    def interviews_scheduled(self):
        return Application.objects.filter(job__company=self.name, status="interview_scheduled").count()

    @property
    def success_rate(self):
        applicants = self.applicants_received
        offers = Application.objects.filter(job__company=self.name, status="offer_received").count()
        return round((offers / applicants) * 100, 2) if applicants > 0 else 0.0
