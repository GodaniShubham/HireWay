from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Job, Application


def student_dashboard(request):
    context = {
        'applied_jobs_count': 5,
        'upcoming_exams_count': 2,
        'placement_status': 'Not Placed',
        'notifications': [
            {'message': 'New job opportunity at XYZ Corp', 'date': '2025-08-29'},
            {'message': 'Upcoming exam reminder: Aptitude Test', 'date': '2025-08-30'},
        ],
    }
    return render(request, 'student_dashboard.html', context)

def company_dashboard(request):
    # Dummy data (you can replace with DB queries later)
    stats = {
        "jobs_posted": 12,
        "applicants": 85,
        "interviews": 14,
        "success_rate": 72,   # percentage
    }

    latest_applicants = [
        {"name": "Alice Johnson", "status": "Shortlisted"},
        {"name": "Rajveer Chavda", "status": "Interview"},
        {"name": "Sarah Lee", "status": "Pending"},
    ]

    return render(request, "company_dashboard.html", {
        "stats": stats,
        "latest_applicants": latest_applicants
    })


def job_applications(request):
    jobs = Job.objects.all()
    # Show applications only for authenticated users, empty list for guests
    applications = Application.objects.filter(user=request.user) if request.user.is_authenticated else []
    
    context = {
        'jobs': jobs,
        'applications': applications,
    }
    return render(request, 'job_applications.html', context)