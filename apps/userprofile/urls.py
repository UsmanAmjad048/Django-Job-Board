# urls.py

from django.urls import path
from .views import dashboard,view_application,view_dashboard_job,delete_job ,all_application,view_cv_file,deleteconversation


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('job/<int:job_id>/', view_dashboard_job, name='view_dashboard_job'),
    path('application/', all_application, name='all_application'),


    path('application/<int:application_id>/', view_application, name='view_application'),
    path('application/<int:application_id>/cv_file/', view_cv_file, name='view_cv_file'),
    path('deleteconversation/<int:pk>', deleteconversation , name='deleteconversation' ),


    path('delete/<int:pk>', delete_job, name='delete'),

]
