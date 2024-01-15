from django.contrib.auth.models import User
from django.db import models
from apps.job.models import Application
import requests

class Userprofile(models.Model):
    user = models. OneToOneField (User, related_name='userprofile', on_delete=models.CASCADE)
    is_employer = models. BooleanField(default=False)
    linkedin_access_token = models.CharField(max_length=255)
    linkedin_sub = models.CharField(max_length=255, unique=True, null=True, blank=True)

    

    def refresh_linkedin_data(self):
        if self.linkedin_access_token:
            linkedin_api_url = 'https://api.linkedin.com/v2/userinfo/'

            headers = {
                'Authorization': f'Bearer {self.linkedin_access_token}',
                'Connection': 'Keep-Alive',
            }

            response = requests.get(linkedin_api_url, headers=headers)

            if response.status_code == 200:
                linkedin_data = response.json()
                
                self.user.first_name = linkedin_data.get('given_name', '')
                self.user.last_name = linkedin_data.get('family_name', '')

                self.user.email = linkedin_data.get('email', self.user.email)
                location = linkedin_data.get('locale', {}).get('country', '')
                language = linkedin_data.get('locale', {}).get('language', '')

                self.save()
                self.user.save()
                data = {
                     'first_name':self.user.first_name,'last_name':self.user.last_name,'email':self.user.email,'location':location, 'language':language,
                }
                return data

            else:
                error_message = response.json().get('message', 'Unknown error')
                print(f"LinkedIn API error: {error_message}")

        else:
            print("No LinkedIn access token for this user.")

User.userprofile = property (lambda u: Userprofile.objects.get_or_create(user=u)[0])

class ConversationMessage(models.Model):
    application = models.ForeignKey(Application, related_name='conversationmessages', on_delete=models.CASCADE)
    content = models.TextField()

    created_by = models.ForeignKey(User, related_name='conversationmessages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']