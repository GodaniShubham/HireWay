from django.urls import path
from . import views

urlpatterns = [
    # Welcome / Landing Page
    path('', views.welcome, name='welcome'),

    # Dashboards
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('company/', views.company_dashboard, name='company_dashboard'),
    path('tpo/', views.tpo_dashboard, name='tpo_dashboard'),

    # Jobs & Applications
    path('jobs/', views.job_applications, name='job_applications'),

    # Company Tests
    path('tests/', views.company_tests, name='company_tests'),         # All tests list page
    path('tests/<int:test_id>/', views.start_test, name='start_test'), # Single test page (Exam)

    # Notifications
    path('notifications/', views.notifications, name='notifications'),
]
