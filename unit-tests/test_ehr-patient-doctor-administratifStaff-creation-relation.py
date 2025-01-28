import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'sihatiBack.settings'

import django
django.setup()
from django.test import TestCase
from api.models import EHR, Doctor, Patient, Hospital, administratifStaff
from datetime import datetime, date


class EHRModelTest(TestCase):
    def setUp(self):
        # Create a hospital for testing
        self.hospital = Hospital.objects.create(
            name="General Hospital"
        )

        # Create a doctor for testing
        self.doctor = Doctor.objects.create(
            name="Dr. John",
            surname="Doe",
            phoneNumber="0123456789",
            specialization="Cardiology",
            email="john.doe@example.com",
            password="securepassword"
        )

        # Create administrative staff for testing
        self.staff = administratifStaff.objects.create(
            name="Admin",
            surname="Smith",
            phoneNumber="0987654321",
            email="admin.smith@example.com",
            password="adminpassword"
        )

        # Create a patient for testing
        self.patient = Patient.objects.create(
            NSS="1234567890",
            name="Jane",
            surname="Doe",
            dateOfBirth=date(1990, 1, 1),
            address="123 Main St",
            phoneNumber="0112233445",
            mutual="HealthPlus",
            contactPerson="John Doe",
            bloodType="A_POSITIVE",
            gender="Female",
            email="jane.doe@example.com",
            profession="Engineer",
            hospital=self.hospital
        )

        # Create an EHR associated with the doctor and staff
        self.ehr = EHR.objects.create(
            creator=self.doctor ,  # Creator is a doctor
            creator_staff=self.staff ,
        )
        
        # Link the EHR to the patient
        self.patient.ehr = self.ehr
        self.patient.save()

    def test_ehr_creation(self):
        # Check if the EHR is created successfully
        ehr = EHR.objects.get(id=self.ehr.id)
        self.assertEqual(ehr.creator.name, "Dr. John")

    def test_doctor_creation(self):
        # Check if the doctor is created successfully
        doctor = Doctor.objects.get(id=self.doctor.id)
        self.assertEqual(doctor.specialization, "Cardiology")

    def test_patient_creation(self):
        # Check if the patient is created successfully
        patient = Patient.objects.get(NSS="1234567890")
        self.assertEqual(patient.name, "Jane")
        self.assertEqual(patient.hospital.name, "General Hospital")

    def test_admin_creation(self):
        # Check if the administrative staff is created successfully
        staff = administratifStaff.objects.get(id=self.staff.id)
        self.assertEqual(staff.name, "Admin")
        self.assertEqual(staff.email, "admin.smith@example.com")

    def test_patient_ehr_link(self):
        # Ensure the patient is linked to the correct EHR
        patient = Patient.objects.get(NSS="1234567890")
        self.assertEqual(patient.ehr.id, self.ehr.id)

    def test_patient_blood_type(self):
        # Check the patient's blood type
        patient = Patient.objects.get(NSS="1234567890")
        self.assertEqual(patient.bloodType, "A_POSITIVE")
