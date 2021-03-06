# Generated by Django 3.1.3 on 2021-01-30 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_auto_20210130_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='father_job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='father_job', to='app.jobs'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mother_job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mother_job', to='app.jobs'),
        ),
    ]
