# Generated by Django 5.2.1 on 2025-05-30 17:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.JSONField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('duration', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=100)),
                ('tags', models.JSONField(default=list)),
                ('organizer', models.CharField(max_length=200)),
                ('contact', models.EmailField(max_length=254)),
                ('isFree', models.BooleanField(default=True)),
                ('ticketPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('imageUrl', models.URLField(max_length=300)),
                ('registrationUrl', models.URLField(blank=True, max_length=300, null=True)),
                ('recurrence', models.CharField(max_length=50)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='user.customuser')),
            ],
        ),
    ]
