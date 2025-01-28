import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'sihatiBack.settings'

import django
django.setup()
from django.test import TestCase
from api.models import EHR, Doctor, Patient, Nurse
from datetime import date


class NurseModelTest(TestCase):
    def setUp(self):
        # Create a doctor for testing
        self.doctor = Doctor.objects.create(
            name="Dr. Alice",
            surname="Smith",
            phoneNumber="1234567890",
            specialization="Pediatrics",
            email="alice.smith@example.com",
            password="securepassword"
        )

        # Create an EHR associated with the doctor
        self.ehr = EHR.objects.create(
            creator=self.doctor,  # Creator is a doctor
        )
        
        # Create a nurse and link the nurse to the EHR
        self.nurse = Nurse.objects.create(
            name="Nurse Nancy",
            surname="Johnson",
            phoneNumber="0987654321",
            email="nancy.johnson@example.com",
            password="nursepassword"
        )
        self.nurse.ehr.add(self.ehr)

    def test_nurse_creation(self):
        # Check if the nurse is created successfully
        nurse = Nurse.objects.get(id=self.nurse.id)
        self.assertEqual(nurse.name, "Nurse Nancy")
        self.assertEqual(nurse.email, "nancy.johnson@example.com")

    def test_nurse_ehr_link(self):
        # Ensure the nurse is linked to the correct EHR
        nurse = Nurse.objects.get(id=self.nurse.id)
        self.assertIn(self.ehr, nurse.ehr.all())
