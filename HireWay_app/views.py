from unittest import TestResult
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib import messages

from django.contrib.auth.models import User

from .models import Company, Job, JobApplication, Notification, Resume, Test,Student,PracticeTest, CompanyTest
  # Import User model from Django
from .forms import ResumeForm, JobApplicationForm, PlacementHistoryForm, EditProfileForm # Correct



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
    company = get_object_or_404(Company, user=request.user)

    jobs_posted = Job.objects.filter(company=company).count()
    applicants = JobApplication.objects.filter(job__company=company).count()
    interviews = JobApplication.objects.filter(job__company=company, status="Interview Scheduled").count()
    offers = JobApplication.objects.filter(job__company=company, status="Offer Received").count()

    stats = {
        "jobs_posted": jobs_posted,
        "applicants": applicants,
        "interviews": interviews,
        "success_rate": round((offers / applicants) * 100, 2) if applicants > 0 else 0,
    }

    latest_applicants = (
        JobApplication.objects.filter(job__company=company)
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
        "total_companies": Company.objects.count(),
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

def practice_and_exam(request):
    # Fetching Practice and Company tests from the database
    practice_tests = PracticeTest.objects.all()
    company_tests = CompanyTest.objects.all()

    return render(request, 'availablemock.html', {
        'practice_tests': practice_tests,
        'company_tests': company_tests
    })

@login_required
def start_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
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
            messages.success(request, "Resume saved successfully!")
            return redirect("resume_detail", pk=resume.pk)
        else:
            print(f"Form errors: {form.errors}")  # Debug
    else:
        form = ResumeForm(initial={
            "full_name": f"{request.user.first_name} {request.user.last_name}".strip() or "Your Name",
            "email": request.user.email or "your.email@example.com",
        })
    return render(request, "resume/resume_form.html", {"form": form})


@login_required
def resume_edit(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == "POST":
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, "Resume updated successfully!")
            return redirect("resume_detail", pk=resume.pk)
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = ResumeForm(instance=resume)
    return render(request, "resume/resume_form.html", {"form": form, "resume": resume})


@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    # pick correct template for display
    template_map = {
        "template1": "resume/pdf_template1.html",
        "template2": "resume/pdf_template2.html",
        "template3": "resume/pdf_template3.html",
    }
    selected_template = template_map.get(resume.template, "resume/pdf_template1.html")

    return render(request, selected_template, {"resume": resume})


@login_required
def resume_pdf(request, pk):
    """Download resume as PDF in selected template"""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    template_map = {
        "template1": "resume/pdf_template1.html",
        "template2": "resume/pdf_template2.html",
        "template3": "resume/pdf_template3.html",
    }
    selected_template = template_map.get(resume.template, "resume/pdf_template1.html")

    html = render_to_string(selected_template, {"resume": resume})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), dest=result)

    if pdf.err:
        return HttpResponse("Error rendering PDF. Please check the template.", status=500)

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{resume.full_name.replace(" ", "_")}_resume.pdf"'
    return response


@login_required
def preview_template(request, template_name):
    """Preview a resume in any template with dummy or form data"""
    preview_data = {
        "resume": {
            "full_name": request.POST.get("full_name", f"{request.user.first_name} {request.user.last_name}" or "John Doe"),
            "email": request.POST.get("email", request.user.email or "john.doe@example.com"),
            "phone": request.POST.get("phone", "9999999999"),
            "college": request.POST.get("college", "Demo University"),
            "course": request.POST.get("course", "Computer Science"),
            "passing_year": request.POST.get("passing_year", "2025"),
            "cgpa": request.POST.get("cgpa", "8.5"),
            "objective": request.POST.get("objective", "Aspiring software engineer looking to contribute."),
            "skills": request.POST.get("skills", "Python, Django, React, SQL"),
            "projects": request.POST.get("projects", "Project 1 - Description\nProject 2 - Description"),
            "certifications": request.POST.get("certifications", "Certification 1\nCertification 2"),
            "template": template_name,
        }
    }

    html = render_to_string(f"resume/pdf_{template_name}.html", preview_data)
    return HttpResponse(html)


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

# --------------------------------------------
# 🔹 Jobs
# --------------------------------------------
@login_required
def job_list(request):
    # Fetch all jobs
    jobs = Job.objects.select_related("company").all()

    # Filters
    domain = request.GET.get("domain")
    package = request.GET.get("package")
    location = request.GET.get("location")

    if domain:
        jobs = jobs.filter(domain__iexact=domain)
    if package:
        jobs = jobs.filter(package__iexact=package)
    if location:
        jobs = jobs.filter(location__iexact=location)

    # Fetch distinct values for dropdowns
    domains = Job.objects.values_list("domain", flat=True).distinct()
    packages = Job.objects.values_list("package", flat=True).distinct()
    locations = Job.objects.values_list("location", flat=True).distinct()

    # Jobs already applied by current user
    my_applications = JobApplication.objects.filter(user=request.user).select_related("job", "job__company")

    context = {
        "jobs": jobs,
        "domains": domains,
        "packages": packages,
        "locations": locations,
        "selected_domain": domain,
        "selected_package": package,
        "selected_location": location,
        "my_applications": my_applications,
    }

    return render(request, "jobs/job_list.html", context)


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    context = {
        'job': job
    }
    return render(request, "jobs/job_detail.html", context)

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobApplicationForm()
    
    context = {
        'form': form,
        'job': job
    }
    return render(request, "jobs/apply_job.html", context)

# Example view for the leaderboard
def leaderboard(request):
    leaderboard_data = [
        {"rank": 1, "name": "Alan Johnson", "score": 950, "badge": "Gold"},
        {"rank": 2, "name": "Paul Garner", "score": 840, "badge": "Silver"},
        {"rank": 3, "name": "John Doe", "score": 780, "badge": "Bronze"},
        {"rank": 4, "name": "Priya Sharma", "score": 710, "badge": "Rising Star"},
    ]
    
    # Passing leaderboard data to the template
    context = {
        'leaderboard': leaderboard_data,
    }
    return render(request, 'leaderboard.html', context)

def placement_history_view(request):
    # Fetch necessary data (dummy data or model-based)
    placement_data = [
        {"name": "John Doe", "status": "Placed", "company": "ABC Corp", "date": "2025-06-01"},
        {"name": "Jane Smith", "status": "Pending", "company": "XYZ Ltd", "date": "2025-06-10"},
    ]

    context = {
        'placement_data': placement_data,
    }

    return render(request, 'placementhistory.html', context)


@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user

    # Assuming you're using Django's built-in User model
    profile_data = {
        'name': user.username,
        'title': 'Software Engineer',  # You could replace this with a dynamic field if you want
        'email': user.email,
        'location': 'New York, NY',  # Replace this with dynamic data if needed
        'about': 'I am a passionate software engineer...',
        'skills': ['JavaScript', 'Python', 'React & Node.js', 'Cloud Computing (AWS, Azure)', 'Machine Learning'],
        'experience': ['Software Engineer at TechCorp', 'Frontend Developer at DevSolutions'],
    }

    return render(request, 'profile.html', {'profile': profile_data})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the form data to update the user's profile
            return redirect('profile')  # Redirect back to the profile page after editing
    else:
        form = EditProfileForm(instance=user)  # If it's a GET request, pre-populate the form with user data

    return render(request, 'edit_profile.html', {'form': form})

# Delete Profile View
@login_required
def delete_profile(request):
    user = request.user
    user.delete()  # This will delete the user profile and the associated user data
    return redirect('welcome')

@login_required
def start_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()

    return render(request, "exam_page.html", {
        "test": test,
        "questions": questions,
    })


@login_required
def submit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()

    correct = 0
    wrong = 0

    for question in questions:
        user_answer = request.POST.get(str(question.id))
        if user_answer:
            if user_answer == question.correct_answer:
                correct += 1
            else:
                wrong += 1

    score = round((correct / questions.count()) * 100, 2)

    # Save result
    TestResult.objects.create(
        user=request.user,
        test=test,
        score=score,
        correct=correct,
        wrong=wrong,
    )

    return render(request, "mockresult.html", {
        "score": score,
        "correct": correct,
        "wrong": wrong,
        "total": questions.count(),
    })
