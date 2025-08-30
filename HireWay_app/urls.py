from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('job_list/', views.job_list, name='job_applications'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
]
