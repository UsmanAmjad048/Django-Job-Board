from django.contrib import admin
from .models import Job , Application # Import your model(s) from the 'models.py' file
admin.site.register(Job)
admin.site.register(Application)

