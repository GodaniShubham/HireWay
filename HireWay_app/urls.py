from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('company/', views.company_dashboard, name='company_dashboard'),
    path('tpo/', views.tpo_dashboard, name='tpo_dashboard'),
    path('jobs/', views.job_applications, name='job_applications'),
    path('company_test/', views.company_tests, name='company_tests'),
    path('exam/<int:test_id>/', views.start_test, name='exam_page'),
    path('notifications/', views.notifications, name='notifications'),
]
