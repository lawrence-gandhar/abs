# Generated by Django 3.1.3 on 2021-01-30 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_complexions'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfilters',
            name='l_complexions',
            field=models.ManyToManyField(blank=True, db_index=True, to='app.Complexions'),
        ),
        migrations.AddField(
            model_name='partner_preferences',
            name='l_complexions',
            field=models.ManyToManyField(blank=True, db_index=True, to='app.Complexions'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='complexion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.complexions'),
        ),
    ]