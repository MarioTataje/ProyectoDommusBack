# Generated by Django 5.0.1 on 2024-05-25 01:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socials', '0006_alter_match_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times_reported', models.IntegerField()),
                ('reason', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('register_date', models.CharField(max_length=10, null=True)),
                ('reported_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_user', to=settings.AUTH_USER_MODEL)),
                ('reporting_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporting_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reports',
            },
        ),
    ]
