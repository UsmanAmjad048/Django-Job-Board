from django.shortcuts import render,redirect , get_object_or_404,HttpResponse
from .models import *
from .form import AddJobForm ,ApplicationForm
from django.contrib.auth.decorators import login_required
from apps.notification.utilities import create_notification


def job_details(request, pk):
    job = Job.objects.get(id=pk)

    return render(request, 'job/jobdetailpage.html', {'job': job})

@login_required
def add_job(request):
    if request.method == 'POST':
        form = AddJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            return redirect('dashboard')
    else:
        
        form = AddJobForm()
    if request.user.userprofile.is_employer == True:
    
        return render(request, 'job/addjob.html', {'form':form})

@login_required
def apply_for_job(request, pk):
    job = Job.objects.get(id=pk)
    user = request.user

    existing_applications = Application.objects.filter(job=job, created_by=user)
    if existing_applications.exists():
        return HttpResponse("You've already applied for this job.")

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.created_by = user

            if 'cv_file' in request.FILES:
                application.cv_file = request.FILES['cv_file']

            application.save()

            create_notification(request, job.created_by, 'application', extra_id=application.id)

            return redirect('dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'job/apply_for_job.html', {'form': form, 'job': job})

    

def search(request):
    return render(request, 'job/search.html')

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, created_by=request.user)

    if request.method == 'POST':
        form = AddJobForm(request.POST, instance=job)

        if form.is_valid():
            job = form.save(commit=False)
            job.status = request.POST.get('status')
            job.save()

            return redirect('dashboard')
    else:
        form = AddJobForm(instance=job)
    
    return render(request, 'job/edit_job.html', {'form': form, 'job': job})
