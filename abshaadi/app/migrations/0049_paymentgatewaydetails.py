# Generated by Django 3.1.3 on 2021-02-19 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_auto_20210130_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGatewayDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('api_link', models.TextField(blank=True, null=True)),
                ('merchant_id', models.CharField(blank=True, max_length=250, null=True)),
                ('api_key', models.CharField(blank=True, max_length=250, null=True)),
                ('api_secret', models.CharField(blank=True, max_length=250, null=True)),
                ('redirect_url', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
