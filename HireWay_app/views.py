from django.shortcuts import render, get_object_or_404
from HireWay_app.models import Job, Application,Notification,Student  # apne models import kar

# 🔹 Welcome Page
def welcome(request):
    return render(request, 'welcome.html')


# 🔹 Student Dashboard
def student_dashboard(request):
    # TODO: yahan baad me Student model se data laa sakte hain
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


# 🔹 Company Dashboard (DB se data)
def company_dashboard(request):
    company_name = request.user.username if request.user.is_authenticated else "Unknown Company"

    jobs_posted = Job.objects.filter(company=company_name).count()
    applicants = Application.objects.filter(job__company=company_name).count()
    interviews = Application.objects.filter(job__company=company_name, status="interview_scheduled").count()
    offers = Application.objects.filter(job__company=company_name, status="offer_received").count()
    success_rate = int((offers / applicants) * 100) if applicants > 0 else 0

    stats = {
        "jobs_posted": jobs_posted,
        "applicants": applicants,
        "interviews": interviews,
        "success_rate": success_rate,
    }

    latest_applicants = (
        Application.objects.filter(job__company=company_name)
        .select_related("user", "job")
        .order_by("-id")[:5]
    )

    context = {
        "stats": stats,
        "latest_applicants": [
            {"name": app.user.username, "status": app.status, "job": app.job.title}
            for app in latest_applicants
        ]
    }
    return render(request, "company.html", context)


# 🔹 TPO Dashboard (abhi dummy, baad me DB connect hoga)
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


# 🔹 Job Applications (dummy for now)
def job_applications(request):
    jobs = Job.objects.all()
    applications = Application.objects.filter(user=request.user) if request.user.is_authenticated else []

    context = {
        'jobs': jobs,
        'applications': applications,
    }
    return render(request, 'job_applications.html', context)


# 🔹 Company Tests (dummy)
def company_tests(request):
    tests = [
        {"id": 1, "company": "TechCorp", "role": "Software Engineer", "date": "Oct 5, 10:00 AM", "duration": 60, "status": "Scheduled"},
        {"id": 2, "company": "FinTechX", "role": "Data Analyst", "date": "Sept 28, 2:00 PM", "duration": 45, "status": "Pending"},
        {"id": 3, "company": "Innovatech", "role": "UI/UX Designer", "date": "Oct 10, 11:00 AM", "duration": 30, "status": "Completed"},
    ]
    return render(request, "company_test.html", {"tests": tests})


# 🔹 Start Test (dummy MCQ test)
def start_test(request, test_id):
    all_tests = {
        1: {
            "title": "TechCorp - Software Engineer Test",
            "time_limit": 60,
            "questions": [
                {"id": 1, "question": "What is the output of 2 + '2' in JavaScript?", "options": ["4", "22", "NaN", "Error"]},
                {"id": 2, "question": "Python is ___ typed language?", "options": ["Strongly", "Weakly", "Dynamically", "Statically"]},
                {"id": 3, "question": "Which company developed React?", "options": ["Google", "Microsoft", "Facebook", "Amazon"]},
            ],
        },
        2: {
            "title": "FinTechX - Data Analyst Test",
            "time_limit": 45,
            "questions": [
                {"id": 1, "question": "Which SQL clause is used to filter records?", "options": ["ORDER BY", "WHERE", "GROUP BY", "JOIN"]},
                {"id": 2, "question": "What is the output of 5 // 2 in Python?", "options": ["2.5", "3", "2", "Error"]},
            ],
        },
        3: {
            "title": "Innovatech - UI/UX Designer Test",
            "time_limit": 30,
            "questions": [
                {"id": 1, "question": "Which tool is widely used for prototyping UI?", "options": ["Photoshop", "Figma", "Excel", "Word"]},
                {"id": 2, "question": "Which color model is used in digital design?", "options": ["CMYK", "RGB", "HSB", "XYZ"]},
            ],
        }
    }

    test = all_tests.get(test_id)
    if not test:
        return render(request, "exam_page.html", {"error": "Test not found!"})

    return render(request, "exam_page.html", {
        "test_id": test_id,
        "title": test["title"],
        "questions": test["questions"],
        "total_questions": len(test["questions"]),
        "time_limit": test["time_limit"],
    })
def notifications(request):
    if not request.user.is_authenticated:
        return render(request, "notifications.html", {"error": "Please log in first"})
    
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None

    all_notifications = Notification.objects.filter(student=student).order_by('-date') if student else []

    return render(request, "notifications.html", {"notifications": all_notifications})