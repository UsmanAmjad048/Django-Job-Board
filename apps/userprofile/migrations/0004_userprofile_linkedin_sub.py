# Generated by Django 5.0.1 on 2024-01-12 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_userprofile_linkedin_access_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='linkedin_sub',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
