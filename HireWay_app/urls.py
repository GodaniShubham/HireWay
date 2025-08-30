from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Landing / Welcome
    path('', views.welcome, name='welcome'),

    # 🔹 Dashboards
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('company/', views.company_dashboard, name='company_dashboard'),
    path('tpo/', views.tpo_dashboard, name='tpo_dashboard'),

    # 🔹 Company Tests / Mock Tests
    path('tests/', views.company_tests, name='company_tests'),
    path('tests/<int:test_id>/', views.start_test, name='start_test'),
    path('result/', views.mocktest_result, name='mocktest_result'),
    path('practice_exam/', views.practice_exam, name='practice_exam'),

    # 🔹 Notifications
    path('notifications/', views.notifications, name='notifications'),

    # 🔹 Resumes
    path('resumes/', views.resume_list, name='resume_list'),
    path('resumes/new/', views.resume_create, name='resume_create'),
    path('resumes/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('resumes/<int:pk>/edit/', views.resume_edit, name='resume_edit'),
    path('resumes/<int:pk>/pdf/', views.resume_pdf, name='resume_pdf'),

    # 🔹 Jobs
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
]