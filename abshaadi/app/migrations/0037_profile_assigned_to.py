# Generated by Django 3.1.3 on 2020-12-06 06:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to_staff', to=settings.AUTH_USER_MODEL),
        ),
    ]
