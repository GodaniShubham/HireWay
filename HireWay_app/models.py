from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# -------------------------------------------------------------------
# 🔹 Student Profile
# -------------------------------------------------------------------
class Student(models.Model):
    PLACEMENT_CHOICES = [
        ("Not Placed", "Not Placed"),
        ("Placed", "Placed"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    applied_jobs_count = models.PositiveIntegerField(default=0)
    upcoming_exams_count = models.PositiveIntegerField(default=0)
    placement_status = models.CharField(max_length=50, choices=PLACEMENT_CHOICES, default="Not Placed")

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return self.user.username


# -------------------------------------------------------------------
# 🔹 Notifications for Students
# -------------------------------------------------------------------
class Notification(models.Model):
    student = models.ForeignKey(Student, related_name="notifications", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.student.user.username} - {self.message[:40]}"


# -------------------------------------------------------------------
# 🔹 Company Profile
# -------------------------------------------------------------------
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_profile")
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

    # 🔹 Dynamic properties
    @property
    def total_jobs(self):
        return Job.objects.filter(company=self).count()

    @property
    def applicants_received(self):
        return JobApplication.objects.filter(job__company=self).count()

    @property
    def interviews_scheduled(self):
        return JobApplication.objects.filter(job__company=self, status="Interview Scheduled").count()

    @property
    def success_rate(self):
        applicants = self.applicants_received
        offers = JobApplication.objects.filter(job__company=self, status="Offer Received").count()
        return round((offers / applicants) * 100, 2) if applicants > 0 else 0.0


# -------------------------------------------------------------------
# 🔹 Test / Exam
# -------------------------------------------------------------------
class Test(models.Model):
    CATEGORY_CHOICES = [
        ("practice", "Practice & Mockup Exam"),
        ("company", "Company Test"),
    ]

    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)  # e.g. "30 mins"
    questions = models.PositiveIntegerField(default=0)
    topics = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="practice")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="beginner")

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    def __str__(self):
        return self.title


# -------------------------------------------------------------------
# 🔹 Resume Builder
# -------------------------------------------------------------------
class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('template1', 'Template 1'),
        ('template2', 'Template 2'),
        ('template3', 'Template 3'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes")
    title = models.CharField(max_length=150, default="My Resume")
    template = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default='template1')

    # Personal
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    address = models.TextField(blank=True)

    # Academic
    college = models.CharField(max_length=250, blank=True)
    course = models.CharField(max_length=150, blank=True)
    passing_year = models.CharField(max_length=10, blank=True)
    cgpa = models.CharField(max_length=10, blank=True)

    # Sections
    objective = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    projects = models.TextField(blank=True, help_text="One project per line: Title - Description")
    certifications = models.TextField(blank=True, help_text="One certification per line")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Resume"
        verbose_name_plural = "Resumes"

    def __str__(self):
        return f"{self.title} ({self.user.username})"


# -------------------------------------------------------------------
# 🔹 Job
# -------------------------------------------------------------------
class Job(models.Model):
    ('title', models.CharField(max_length=255, default='')), # Ensure this exists
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    domain = models.CharField(max_length=100, blank=True)
    package = models.CharField(max_length=50, blank=True)
    deadline = models.DateField()

    def __str__(self):
        return f"{self.title} at {self.company.name}"  # This references job.title





# -------------------------------------------------------------------
# 🔹 Job Application
# -------------------------------------------------------------------
class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)
    enrollment_number = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    passing_year = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()

    STATUS_CHOICES = [
        ('Shortlisted', 'Shortlisted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Offer Received', 'Offer Received'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Shortlisted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"

