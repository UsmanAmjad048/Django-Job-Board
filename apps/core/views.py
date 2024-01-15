from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from apps.job.models import Job
from apps.userprofile.models import Userprofile






def frontpage(request):
    job = Job.objects.all()

    return render(request, 'core/frontpage.html', {'jobs': job})


def signuppage(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user_type = request.POST.get('userType', 'jobseeker')
            if user_type == 'employer':
                user_profile = Userprofile.objects.create(
                    user=user, is_employer=True)
                user_profile.save()
            else:
                user_profile = Userprofile.objects.create(user=user)
                user_profile.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("frontpage")

        else:
            return render(request, 'core/signuppage.html', {'form': form})

    else:
        form = UserCreationForm()

    return render(request, 'core/signuppage.html', {'form': form})


def login_view(request):
    print(request,'requestrequestrequest')
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("frontpage")

    return render(request, 'core/loginpage.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('frontpage')
