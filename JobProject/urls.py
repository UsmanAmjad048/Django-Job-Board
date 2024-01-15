# urls.py

from django.contrib import admin
from django.urls import path , include
from apps.core.views import frontpage, signuppage


from apps.core.views import login_view, custom_logout
from . import views
from .views import ContactView


from django.urls import path




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name='frontpage'),
    path('signup/', signuppage, name='signup'),
    path('logout/', custom_logout, name='logout'),
    path('login/', login_view, name='login'),
    path('contact/', ContactView.as_view(), name='contact'),

    path('dashboard/', include('apps.userprofile.urls')),
    path('jobs/', include('apps.job.urls')),
    path('notifications/', include('apps.notification.urls')),
    path('social-auth/', include('social_django.urls'),name='social'),
    path('linkedin-auth/', views.linkedin_auth, name='linkedin_auth'),
    path('complete/linkedin-oauth2/', views.linkedin_callback, name='linkedin_callback'),


]




