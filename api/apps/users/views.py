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
from api.models import (
    Patient, EHR, Doctor, administratifStaff, Nurse, Radiologist, LabTechnician, Hospital,
    BiologyReport, RadiologyReport, Prescription, Diagnostic, Consultation, MedicalCertificate, 
    CareProvided, Observation, MedicationAdministered
)
from api.helper.getModels import getModel



@method_decorator(csrf_exempt, name='dispatch')
class UpdateProfileView(View):
    def put(self, request):
        # Extract and validate the Authorization token
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            # Decode token
            token = token.split(" ")[1]  # Assuming Bearer Token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded.get("role", "").strip().lower()
            user_id = decoded.get("user_id")

            # Validate role
            valid_roles = ['administratifstaff', 'nurse', 'doctor', 'radiologist', 'labtechnician', 'patient']
            if role not in valid_roles:
                return JsonResponse({"error": "Unauthorized role"}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # Parse input data
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        # Process update based on role
        try:
            if role in ['administratifstaff', 'nurse', 'doctor', 'radiologist', 'labtechnician']:
                # Update staff profile
                model = {
                    'administratifstaff': administratifStaff,
                    'nurse': Nurse,
                    'doctor': Doctor,
                    'radiologist': Radiologist,
                    'labtechnician': LabTechnician
                }[role]

                user = model.objects.get(id=user_id)
                user.name = data.get('name', user.name)
                user.surname = data.get('surname', user.surname)
                user.phoneNumber = data.get('phoneNumber', user.phoneNumber)
                user.email = data.get('email', user.email)
                if 'password' in data:
                    user.password = data['password']
                user.save()

            elif role == 'patient':
                # Update patient profile
                user = Patient.objects.get(id=user_id)
                user.email = data.get('email', user.email)
                user.phoneNumber = data.get('phoneNumber', user.phoneNumber)
                if 'password' in data:
                    user.password = data['password']
                user.save()

            return JsonResponse({"message": "Profile updated successfully"}, status=200)

        except model.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
      
      
@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(View):

    def get(self, request):
        # Extract and validate the Authorization token
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            # Decode token
            token = token.split(" ")[1]  # Assuming Bearer Token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded.get("role", "").strip().lower()
            user_id = decoded.get("user_id")

            # Validate role
            valid_roles = ['administratifstaff', 'nurse', 'doctor', 'radiologist', 'labtechnician', 'patient']
            if role not in valid_roles:
                return JsonResponse({"error": "Unauthorized role"}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # Fetch user profile based on role
        try:
            if role in ['administratifstaff', 'nurse', 'doctor', 'radiologist', 'labtechnician']:
                model = {
                    'administratifstaff': administratifStaff,
                    'nurse': Nurse,
                    'doctor': Doctor,
                    'radiologist': Radiologist,
                    'labtechnician': LabTechnician
                }[role]

                user = model.objects.get(id=user_id)
                profile_data = {
                    'name': user.name,
                    'surname': user.surname,
                    'phoneNumber': user.phoneNumber,
                    'email': user.email,
                    'role': role
                }

                # Additional info for doctors, radiologists, lab technicians
                if role in ['doctor', 'radiologist', 'labtechnician']:
                    profile_data.update({
                        'specialization': user.specialization,
                    })

            elif role == 'patient':
                try:
                    # Fetch the patient and their EHR record
                    patient = Patient.objects.get(id=user_id)

                    # Retrieve profile data
                    profile_data = {
                        'name': patient.name,
                        'surname': patient.surname,
                        'phoneNumber': patient.phoneNumber,
                        'email': patient.email,
                        'role': role,
                    }

                    # Get the doctor from the EHR creator
                    if patient.ehr.creator:
                        doctor = patient.ehr.creator
                        profile_data.update({
                            'doctorName': doctor.name,
                            'doctorSurname': doctor.surname,
                            'hospitalName': patient.hospital.name,
                        })

                    # Include NSS if available
                    profile_data['nss'] = patient.NSS if hasattr(patient, 'NSS') else None

                   

                except Patient.DoesNotExist:
                    return JsonResponse({"error": "Patient not found"}, status=404)
                except EHR.DoesNotExist:
                    return JsonResponse({"error": "EHR not found for this patient"}, status=404)
                except Hospital.DoesNotExist:
                    return JsonResponse({"error": "Hospital not found for this patient"}, status=404)

            return JsonResponse({"profile": profile_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
