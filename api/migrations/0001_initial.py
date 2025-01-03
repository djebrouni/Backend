# Generated by Django 5.1.4 on 2025-01-03 00:25

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='administratifStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('surname', models.CharField(max_length=45)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=70)),
                ('password', models.CharField(max_length=200)),
                ('role', models.CharField(default='administratifStaff', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Diagnostic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('surname', models.CharField(max_length=45)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('specialization', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=70)),
                ('password', models.CharField(max_length=200)),
                ('role', models.CharField(default='doctor', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='LabTechnician',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('surname', models.CharField(max_length=45)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('specialization', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=70)),
                ('password', models.CharField(max_length=200)),
                ('role', models.CharField(default='LabTechnician', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Medecine',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Radiologist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('surname', models.CharField(max_length=45)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('specialization', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=70)),
                ('password', models.CharField(max_length=200)),
                ('role', models.CharField(default='Radiologist', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='sgph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=70)),
                ('password', models.CharField(max_length=200)),
                ('role', models.CharField(default='sgph', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('summary', models.TextField()),
                ('chiefComplaint', models.TextField()),
                ('done', models.BooleanField(default=False)),
                ('diagnostic', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultation', to='api.diagnostic')),
            ],
        ),
        migrations.CreateModel(
            name='EHR',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_ehrs', to='api.doctor')),
                ('creator_staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_ehrs', to='api.administratifstaff')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='ehr',
            field=models.ManyToManyField(blank=True, related_name='doctors', to='api.ehr'),
        ),
        migrations.CreateModel(
            name='CareProvided',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('care_actions', models.TextField()),
                ('ehr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='care_provided', to='api.ehr')),
            ],
        ),
        migrations.CreateModel(
            name='BiologyReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bloodSugarLevel', models.FloatField()),
                ('bloodPressure', models.FloatField()),
                ('cholesterolLevel', models.FloatField()),
                ('completeBloodCount', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biology_reports', to='api.doctor')),
                ('ehr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biology_reports', to='api.ehr')),
                ('lab_technician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biology_reports', to='api.labtechnician')),
            ],
        ),
        migrations.CreateModel(
            name='BiologicalAssessment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('patient_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('tests_to_conduct', models.TextField()),
                ('biology_report', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessment', to='api.biologyreport')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biological_assessments', to='api.doctor')),
                ('ehr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biological_assessments', to='api.ehr')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalCertificate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('requesed', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_certificates', to='api.doctor')),
                ('ehr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_certificates', to='api.ehr')),
            ],
        ),
        migrations.CreateModel(
            name='MedicationAdministered',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('care_provided', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medications_administered', to='api.careprovided')),
                ('medicine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.medecine')),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('surname', models.CharField(max_length=45)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=70)),
                ('password', models.CharField(max_length=200)),
                ('role', models.CharField(default='Nurse', max_length=50)),
                ('ehr', models.ManyToManyField(blank=True, related_name='nurses', to='api.ehr')),
            ],
        ),
        migrations.AddField(
            model_name='careprovided',
            name='nurse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='care_provided', to='api.nurse'),
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('care_provided', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='api.careprovided')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('NSS', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=45)),
                ('surname', models.CharField(max_length=45)),
                ('dateOfBirth', models.DateField(null=True)),
                ('address', models.CharField(blank=True, max_length=70)),
                ('phoneNumber', models.CharField(blank=True, max_length=10)),
                ('mutual', models.CharField(blank=True, max_length=45)),
                ('contactPerson', models.CharField(blank=True, max_length=45)),
                ('bloodType', models.CharField(choices=[('A_POSITIVE', 'A+'), ('A_NEGATIVE', 'A-'), ('B_POSITIVE', 'B+'), ('B_NEGATIVE', 'B-'), ('AB_POSITIVE', 'AB+'), ('AB_NEGATIVE', 'AB-'), ('O_POSITIVE', 'O+'), ('O_NEGATIVE', 'O-')], default='O_POSITIVE', max_length=11)),
                ('gender', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('profession', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(default='Patient', max_length=50)),
                ('ehr', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient', to='api.ehr')),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='api.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('isValid', models.BooleanField(default=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='api.doctor')),
                ('ehr', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='api.ehr')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalTreatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dose', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('Duration', models.IntegerField(default=0)),
                ('medicine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.medecine')),
                ('prescription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_treatments', to='api.prescription')),
            ],
        ),
        migrations.AddField(
            model_name='diagnostic',
            name='prescription',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diagnostic', to='api.prescription'),
        ),
        migrations.CreateModel(
            name='RadiologyReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Type', models.CharField(max_length=45)),
                ('imageData', models.ImageField(blank=True, null=True, upload_to='radiology_reports/')),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('doctor', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='radiology_reports', to='api.doctor')),
                ('ehr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='radiology_reports', to='api.ehr')),
                ('radiologist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='radiology_reports', to='api.radiologist')),
            ],
        ),
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
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='radiology_assessments', to='api.doctor')),
                ('ehr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radiology_assessments', to='api.ehr')),
                ('radiology_report', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessment', to='api.radiologyreport')),
            ],
        ),
    ]
