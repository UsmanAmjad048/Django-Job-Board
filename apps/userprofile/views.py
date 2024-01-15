from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.job.models import Job, Application
from .models import ConversationMessage

from django.http import HttpResponse
from django.conf import settings
import os

from apps.notification.utilities import create_notification
# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'userprofile/dashboard.html', {'userprofile': request.user.userprofile})


@login_required
def view_application(request, application_id):
    if request.user.userprofile.is_employer:
        application = get_object_or_404(
            Application, pk=application_id, job__created_by=request.user)
    else:
        application = get_object_or_404(
            Application, pk=application_id, created_by=request.user)

    if request.method == 'POST':
        content = request.POST.get('content')
        message = request.POST.get('message')

        if content:
            conversationmessage = ConversationMessage.objects.create(
                application=application, content=content, created_by=request.user)

            create_notification(request, application.created_by,
                                'message', extra_id=application.id)

            return redirect('view_application', application_id=application_id)
        elif message:
            conversationmessage = ConversationMessage.objects.create(
                application=application, content=message, created_by=request.user)

            create_notification(request, application.created_by,
                                'message', extra_id=application.id)

            return redirect('view_application', application_id=application_id)

    return render(request, 'userprofile/view_application.html', {'application': application})


@login_required
def view_dashboard_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, created_by=request.user)
    if request.user.userprofile.is_employer:

        return render(request, 'userprofile/view_dashboard_job.html', {'job': job})


@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, id=pk, created_by=request.user)
    if request.user.userprofile.is_employer:
        job.delete()

        return redirect('dashboard')


@login_required
def all_application(request):
    if request.user.userprofile.is_employer:
        jobs_created_by_user = Job.objects.filter(created_by=request.user)
        job_applications = Application.objects.filter(
            job__in=jobs_created_by_user)

        return render(request, 'userprofile/job_applications.html', {'job_applications': job_applications})


def view_cv_file(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    cv_file_path = application.cv_file.path

    if os.path.exists(cv_file_path):
        with open(cv_file_path, 'rb') as file:
            response = HttpResponse(
                file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(cv_file_path)
            return response
    else:
        return HttpResponse("File not found", status=404)


@login_required
def deleteconversation(request, pk):
    conversation = get_object_or_404(ConversationMessage, id=pk)
    if request.user == conversation.created_by:
        conversation.delete()
        return redirect('view_application', application_id=conversation.application.id)


@login_required
def refresh_linkedin_data(request):
    if request.user.userprofile.linkedin_access_token:
        user_data = request.user.userprofile.refresh_linkedin_data()
        print(user_data,'user_data')
        request.session['user_data'] = user_data
        return redirect(request.META.get('HTTP_REFERER', '/default-redirect-url/'))
    else:
        return redirect('')
