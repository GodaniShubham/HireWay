from django.contrib import admin
from .models import Student, Notification, Job, JobApplication, Company, Resume, PracticeTest, CompanyTest

# Student Model Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "applied_jobs_count", "upcoming_exams_count", "placement_status")

# Notification Model Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("student", "message", "date")

# Job Model Admin
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "package", "domain", "salary", "deadline")

# Job Application Model Admin
@admin.register(JobApplication)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "status")

# Company Model Admin
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "total_jobs", "applicants_received", "interviews_scheduled", "success_rate")

# Resume Model Admin
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'full_name', 'user', 'template', 'updated_at')
    list_filter = ('template', 'updated_at')
    search_fields = ('full_name', 'email', 'user__username')


admin.site.register(PracticeTest)
admin.site.register(CompanyTest)