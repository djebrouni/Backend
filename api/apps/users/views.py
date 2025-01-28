from django.shortcuts import render
import json
import jwt
import re
from datetime import datetime
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from api.const.ROLES import ROLES
from api.models import (
    Patient, EHR, Doctor, administratifStaff, Nurse, Radiologist, LabTechnician, Hospital,
    BiologyReport, RadiologyReport, Prescription, Diagnostic, Consultation, MedicalCertificate, 
    CareProvided, Observation, MedicationAdministered
)
from api.helper.getModels import getModel
from api.middlewares.authentication import verify_user


@method_decorator(csrf_exempt, name='dispatch')
class UpdateProfileView(View):
    @verify_user
    def put(self, request):
        # get from middleware
        user = request.user
        role = request.role
        Model = request.Model

        # Parse input data
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        # Process update based on role
        try:
            # for NON patient users
            if role != ROLES.Patient.value:
                user.name = data.get('name', user.name)
                user.surname = data.get('surname', user.surname)
                
            user.email = data.get('email', user.email)
            user.phoneNumber = data.get('phoneNumber', user.phoneNumber)
            if 'password' in data:
                user.password = data['password']
            user.save()

            return JsonResponse({"message": "Profile updated successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
      
      
@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(View):
    @verify_user
    def get(self, request):
        # get from middleware
        user = request.user
        role = request.role
        Model = request.Model

        # send user profile based on role
        try:
            profile_data = {
                'name': user.name,
                'surname': user.surname,
                'phoneNumber': user.phoneNumber,
                'email': user.email,
            }
               
            # Additional info for doctors, radiologists, lab technicians
            if role in [ROLES.Doctor.value, ROLES.Radiologist.value, ROLES.LabTechnician.value]:
                profile_data.update({
                    'specialization': user.specialization,
                })

            elif role == ROLES.Patient.value:
                try:
                    # Get the doctor from the EHR creator
                    if user.ehr.creator:
                        doctor = user.ehr.creator
                        profile_data.update({
                            'doctorName': doctor.name,
                            'doctorSurname': doctor.surname,
                            'hospitalName': user.hospital.name,
                        })

                    # Include NSS if available
                    profile_data['nss'] = user.NSS if hasattr(user, 'NSS') else None

                except EHR.DoesNotExist:
                    return JsonResponse({"error": "EHR not found for this patient"}, status=404)
                except Hospital.DoesNotExist:
                    return JsonResponse({"error": "Hospital not found for this patient"}, status=404)

            return JsonResponse({"profile": profile_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
