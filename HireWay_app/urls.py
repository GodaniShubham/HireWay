from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path("company/", views.company_dashboard, name="company_dashboard"),
    path('jobs/', views.job_applications, name='job_applications'),

]
