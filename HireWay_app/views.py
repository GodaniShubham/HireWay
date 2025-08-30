from django.shortcuts import render

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
    stats = {
        "jobs_posted": 12,
        "applicants": 85,
        "interviews": 14,
        "success_rate": 72,
    }

    latest_applicants = [
        {"name": "Alice Johnson", "status": "Shortlisted"},
        {"name": "Rajveer Chavda", "status": "Interview"},
        {"name": "Sarah Lee", "status": "Pending"},
    ]

    return render(request, "company.html", {
        "stats": stats,
        "latest_applicants": latest_applicants
    })

def tpo_dashboard(request):
    stats = {
        "total_companies": 25,
        "students_registered": 320,
        "placements_done": 145,
        "ongoing_drives": 6,
    }

    latest_drives = [
        {"company": "Google", "role": "SDE", "date": "2025-09-02"},
        {"company": "Amazon", "role": "Data Analyst", "date": "2025-09-05"},
        {"company": "Infosys", "role": "System Engineer", "date": "2025-09-08"},
    ]

    return render(request, "tpo.html", {
        "stats": stats,
        "latest_drives": latest_drives,
    })




def job_applications(request):
    # Dummy data for now
    jobs = [
        {"title": "Software Engineer", "company": "Google"},
        {"title": "Data Analyst", "company": "Amazon"},
    ]
    applications = []

    context = {
        'jobs': jobs,
        'applications': applications,
    }
    return render(request, 'job_applications.html', context)

def company_tests(request):
    tests = [
        {"company": "TechCorp", "role": "Software Engineer", "date": "Oct 5, 10:00 AM", "duration": 60, "status": "Scheduled"},
        {"company": "FinTechX", "role": "Data Analyst", "date": "Sept 28, 2:00 PM", "duration": 45, "status": "Pending"},
        {"company": "Innovatech", "role": "UI/UX Designer", "date": "Oct 10, 11:00 AM", "duration": 30, "status": "Completed"},
    ]
    return render(request, "company_tests.html", {"tests": tests})
