# urls.py

from django.urls import path
from .api import api_search

from .views import add_job,job_details,apply_for_job , search , edit_job
from apps.userprofile.views import refresh_linkedin_data


urlpatterns = [
    path('api/search/', api_search, name='api_search'),
    path('search/', search, name='search'),
    path('addjob/', add_job, name='addjob'),
    path('<int:pk>/',job_details , name='job_detail'),
    path('<int:job_id>/edit/', edit_job, name='edit_job'),

    path('<int:pk>/apply_for_job/', apply_for_job, name='apply_for_job'),
    path('refresh_linkedin_data/', refresh_linkedin_data, name='refresh_linkedin_data'),


]
