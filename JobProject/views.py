from django.conf import settings
from django.shortcuts import redirect,render
import secrets
from django.conf import settings
import requests
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from apps.job.models import Job
from django.contrib.auth import authenticate, login

from apps.userprofile.models import Userprofile


def linkedin_auth(request):
    redirect_uri = 'http://localhost:8080/complete/linkedin-oauth2/'
    state_value = secrets.token_urlsafe(16)
    scope_values = 'profile email w_member_social openid'

    redirect_url = f"https://www.linkedin.com/oauth/v2/authorization?client_id={settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY}&redirect_uri={redirect_uri}&response_type=code&state={state_value}&scope={scope_values}"
    return redirect(redirect_url)

def linkedin_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
   
    if code and state:
        access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        redirect_uri = 'http://localhost:8080/complete/linkedin-oauth2/'
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY,
            'client_secret': settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET
        }

        response = requests.post(access_token_url, data=payload)

        if response.status_code == 200:
            access_token = response.json().get('access_token')
            profile_endpoint = 'https://api.linkedin.com/v2/userinfo/'

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Connection': 'Keep-Alive'
            }

            response = requests.get(profile_endpoint, headers=headers)
            if response.status_code == 403:
                error_message = response.json().get('message', 'Permission not allowed')
                print(f"Permission error: {error_message}")

            if response.status_code == 200:
                profile_data = response.json()
                linkedin_sub = profile_data.get('sub')


                try:
                    user_profile = Userprofile.objects.get(linkedin_sub=linkedin_sub)
                    user = user_profile.user
                except Userprofile.DoesNotExist:
                    try:
                        user = User.objects.get(email=profile_data.get('email'))
                    except User.DoesNotExist:
                        user = User.objects.create_user(
                            username=profile_data.get('name'),
                            email=profile_data.get('email'),
                            password=User.objects.make_random_password(),
                        )

                    Userprofile.objects.create(user=user, linkedin_sub=linkedin_sub, linkedin_access_token=access_token)

                user = authenticate(request, username=user.username, password=user.username)
                login(request, user)

                return redirect('dashboard')
        else:
            error_message = response.json().get('error_description', 'Unknown error')
            return render(request, 'job/error.html', {'error_message': error_message})
    else:
        return render(request, 'job/error.html', {'error_message': 'Invalid URL parameters'})

from django.shortcuts import render
from django.views import View

class ContactView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'core/contact.html')
