from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from xhtml2pdf import pisa
from io import BytesIO

from .models import Job, Application, Notification, Student, Test, Resume
from .forms import ResumeForm


# --------------------------------------------
# 🔹 Public / General Views
# --------------------------------------------
def welcome(request):
    return render(request, "welcome.html")


# --------------------------------------------
# 🔹 Student Dashboard
# --------------------------------------------
@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None

    context = {
        "applied_jobs_count": student.applied_jobs_count if student else 0,
        "upcoming_exams_count": student.upcoming_exams_count if student else 0,
        "placement_status": student.placement_status if student else "Not Registered",
        "notifications": Notification.objects.filter(student=student).order_by("-date")[:5] if student else [],
    }
    return render(request, "student_dashboard.html", context)


# --------------------------------------------
# 🔹 Company Dashboard
# --------------------------------------------
@login_required
def company_dashboard(request):
    company_name = request.user.username if request.user.is_authenticated else "Unknown"

    jobs_posted = Job.objects.filter(company=company_name).count()
    applicants = Application.objects.filter(job__company=company_name).count()
    interviews = Application.objects.filter(job__company=company_name, status="interview_scheduled").count()
    offers = Application.objects.filter(job__company=company_name, status="offer_received").count()

    stats = {
        "jobs_posted": jobs_posted,
        "applicants": applicants,
        "interviews": interviews,
        "success_rate": round((offers / applicants) * 100, 2) if applicants > 0 else 0,
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
        ],
    }
    return render(request, "company_dashboard.html", context)


# --------------------------------------------
# 🔹 TPO Dashboard
# --------------------------------------------
@login_required
def tpo_dashboard(request):
    stats = {
        "total_companies": 25,
        "students_registered": Student.objects.count(),
        "placements_done": Student.objects.filter(placement_status="Placed").count(),
        "ongoing_drives": Job.objects.count(),
    }

    latest_drives = Job.objects.order_by("-id")[:5]

    return render(request, "tpo_dashboard.html", {"stats": stats, "latest_drives": latest_drives})


# --------------------------------------------
# 🔹 Tests & Exams
# --------------------------------------------
@login_required
def company_tests(request):
    tests = Test.objects.filter(category="company").order_by("-id")
    return render(request, "company_test.html", {"tests": tests})


@login_required
def practice_exam(request):
    practice_tests = Test.objects.filter(category="practice").order_by("difficulty")
    company_tests = Test.objects.filter(category="company").order_by("difficulty")
    return render(request, "availablemock.html", {
        "practice_tests": practice_tests,
        "company_tests": company_tests
    })


@login_required
def start_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    # Dummy questions (later replace with real model)
    base_questions = [
        {"question": "What is the output of 2 + '2' in JavaScript?", "options": ["4", "22", "NaN", "Error"]},
        {"question": "Python is ___ typed language?", "options": ["Strongly", "Weakly", "Dynamically", "Statically"]},
        {"question": "Which company developed React?", "options": ["Google", "Microsoft", "Facebook", "Amazon"]},
    ]

    questions = []
    for i in range(test.questions):
        q = base_questions[i % len(base_questions)].copy()
        q["id"] = i + 1
        q["question"] = f"Q{i+1}. {q['question']}"
        questions.append(q)

    return render(request, "exam_page.html", {
        "test": test,
        "questions": questions,
        "total_questions": len(questions),
    })


@login_required
def mocktest_result(request):
    # Dummy result
    result_data = {
        "score": 77.5,
        "correct": 21,
        "wrong": 9,
        "sections": [
            {"name": "Aptitude", "correct": 7, "wrong": 3, "score": 70},
            {"name": "Reasoning", "correct": 8, "wrong": 2, "score": 80},
            {"name": "English", "correct": 6, "wrong": 4, "score": 60},
            {"name": "Coding", "correct": 2, "wrong": 0, "score": 100},
        ],
    }
    return render(request, "mockresult.html", {"result": result_data})


# --------------------------------------------
# 🔹 Resume Builder
# --------------------------------------------
@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, "resume/resume_list.html", {"resumes": resumes})


@login_required
def resume_create(request):
    if request.method == "POST":
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect("resume_detail", pk=resume.pk)
    else:
        form = ResumeForm(initial={
            "full_name": f"{request.user.first_name} {request.user.last_name}".strip(),
            "email": getattr(request.user, "email", ""),
        })
    return render(request, "resume/resume_form.html", {"form": form})


@login_required
def resume_edit(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == "POST":
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect("resume_detail", pk=resume.pk)
    else:
        form = ResumeForm(instance=resume)
    return render(request, "resume/resume_form.html", {"form": form, "resume": resume})


@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, "resume/resume_detail.html", {"resume": resume})


@login_required
def resume_pdf(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    html = render_to_string(f"resume/pdf_{resume.template}.html", {"resume": resume, "user": request.user})

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), dest=result)
    if pdf.err:
        return HttpResponse("Error rendering PDF", status=500, content_type="text/plain")

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{resume.full_name.replace(" ", "_")}_resume.pdf"'
    return response
@login_required
def notifications(request):
    student = None
    notifications = []

    try:
        student = Student.objects.get(user=request.user)
        notifications = Notification.objects.filter(student=student).order_by("-date")
    except Student.DoesNotExist:
        pass

    return render(request, "notifications.html", {"notifications": notifications})

