from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('company/', views.company_dashboard, name='company_dashboard'),
    path('tpo/dashboard/', views.tpo_dashboard, name='tpo_dashboard'),
    path('company/tests/', views.company_tests, name='company_tests'),
    path("practice-exam/", views.practice_and_exam, name="practice_exam"),
    path("test/<int:test_id>/start/", views.start_test, name="start_test"),
    path("test/<int:test_id>/submit/", views.submit_test, name="submit_test"),
    path('start-test/<int:test_id>/', views.start_test, name='start_test'),
    path('mocktest-result/', views.mocktest_result, name='mocktest_result'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('resumes/new/', views.resume_create, name='resume_create'),
    path('resumes/<int:pk>/edit/', views.resume_edit, name='resume_edit'),
    path('resumes/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('resumes/<int:pk>/pdf/', views.resume_pdf, name='resume_pdf'),
    path('preview-template/<str:template_name>/', views.preview_template, name='preview_template'),
    path('notifications/', views.notifications, name='notifications'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('leader/', views.leaderboard, name='leaderboard'),
    path('history/', views.placement_history_view, name='placement_history'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit profile page
    path('profile/delete/', views.delete_profile, name='delete_profile'),

]