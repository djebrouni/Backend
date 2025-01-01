# Generated by Django 5.1.4 on 2025-01-01 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_biologicalassessment_doctor'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadiologyAssessment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('patient_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('imaging_type', models.CharField(max_length=255)),
                ('ehr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radiology_assessments', to='api.ehr')),
            ],
        ),
    ]
