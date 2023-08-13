from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobForm, CreateJobForm
from .models import Job
from django.contrib import messages


def job_list(request):
    jobs = Job.objects.all()  # We retrieve all the jobs from the database with this line
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def edit_job(request, job_id):
    print("Processing edit_job view")  # This will print every time the view is accessed
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        print("Received a POST request")  # This will print every time a POST request is received
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            print("Form is valid, job saved")  # This will print every time the form is valid and the job is saved
            messages.success(request, 'Job saved successfully')  # displayed for the user
            return redirect('job_list')

        else:
            messages.error(request, 'There was an error saving the job')
            print("Form is not valid, errors:", form.errors)  # This will print every time the form is not valid
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form})


def job_listing(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    form = JobForm(instance=job)
    if form.is_valid():
        return redirect('job_list')
    else:
        print("Form is not valid, errors:", form.errors)
    return render(request, 'jobs/job_listing.html', {'form': form})


def create_job(request):
    print("Processing create_job view")  # This will print every time the view is accessed
    if request.method == 'POST':
        print("Received a POST request")  # This will print every time a POST request is received
        form = CreateJobForm(request.POST)  # >> changing job form <<
        if form.is_valid():
            form.save()
            print("Form is valid, job saved")  # This will print every time the form is valid and the job is saved
            messages.success(request, 'Job created successfully')  # displayed for the user
            return redirect('job_list')
        else:
            messages.error(request, 'There was an error creating the job')
            print("Form is not valid, errors:", form.errors)  # This will print every time the form is not valid
    else:
        form = CreateJobForm()  # No instance is passed, as this is for creating a new job
    return render(request, 'jobs/create_job.html', {'form': form})


