from django import forms
from .models import Resume, JobApplication

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'title', 'template', 'full_name', 'email', 'phone', 'address',
            'college', 'course', 'passing_year', 'cgpa', 'objective',
            'skills', 'projects', 'certifications'
        ]
        widgets = {
            'objective': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 4}),
            'projects': forms.Textarea(attrs={'rows': 4}),
            'certifications': forms.Textarea(attrs={'rows': 4}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'enrollment_number', 'branch', 'passing_year', 'email', 'phone', 'resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }