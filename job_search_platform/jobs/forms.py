from django import forms
from django.core.exceptions import ValidationError
from .models import Job


class JobForm(forms.ModelForm):
    error_css_field = 'error-field'
    required_css_class = 'required-field'
    # be aware: Using widget here will oblige all classes who inherits from this class to also have "title" field
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "job title"}))

    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'description', 'min_salary', 'max_salary']

    def __init__(self, *args, **kwargs):  # moving widget here to avoid using in all classes inheriting from this class
        super(JobForm, self).__init__(*args, **kwargs)
        if 'description' in self.fields:  # Only modify the widget if the description field is present
            self.fields['description'].widget = forms.TextInput(attrs={"rows": "10"})

    def clean_min_salary(self):
        min_salary = self.cleaned_data.get('min_salary')
        if min_salary <= 1000:
            raise ValidationError("Salary too low")
        return min_salary



# Creating a separated class for handling the create job function, it inherits from "JobForm" and overrides its fields
class CreateJobForm(JobForm):
    class Meta(JobForm.Meta):  # Inheriting the Meta class from JobForm
        fields = ['title', 'company', 'location']  # Only these fields will be included

    def __init__(self, *args, **kwargs):
        super(CreateJobForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['company'].required = True
        self.fields['location'].required = True

