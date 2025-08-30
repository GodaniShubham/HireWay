from django.contrib import admin
from .models import Student, Notification, Job, Application, Company

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "applied_jobs_count", "upcoming_exams_count", "placement_status")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("student", "message", "date")

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "package", "domain")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "status")

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "total_jobs", "applicants_received", "interviews_scheduled", "success_rate")



# admin.py
from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title','full_name','user','template','updated_at')
    list_filter = ('template','updated_at')
    search_fields = ('full_name','email','user__username')
