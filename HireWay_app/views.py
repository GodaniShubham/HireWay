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


def job_list(request):
    jobs = Job.objects.all()
    applications = []

    if request.user.is_authenticated:
        applications = Application.objects.filter(user=request.user)

    return render(request, "job_applications.html", {
        "jobs": jobs,
        "applications": applications
    })


def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.is_authenticated:
        Application.objects.create(user=request.user, job=job, status="Applied")
    else:
        print("Anonymous user tried to apply.")

    return redirect("job_applications")
