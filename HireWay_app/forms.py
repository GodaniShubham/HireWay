from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            "title", "template",
            "full_name", "email", "phone", "address",
            "college", "course", "passing_year", "cgpa",
            "objective", "skills", "projects", "certifications"
        ]
        widgets = {
            "objective": forms.Textarea(attrs={"rows":4}),
            "skills": forms.Textarea(attrs={"rows":3}),
            "projects": forms.Textarea(attrs={"rows":4}),
            "certifications": forms.Textarea(attrs={"rows":3}),
            "address": forms.Textarea(attrs={"rows":2}),
        }
