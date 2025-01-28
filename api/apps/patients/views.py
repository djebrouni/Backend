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
from api.middlewares.authentication import verify_user
from api.middlewares.authorization import verify_role
from api.models import (
    Patient, EHR, Doctor, administratifStaff, Nurse, Radiologist, LabTechnician, Hospital,
    BiologyReport, RadiologyReport, Prescription, Diagnostic, Consultation, MedicalCertificate, 
    CareProvided, Observation, MedicationAdministered
)
from api.helper.getModels import getModel

import jwt
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from api.models import Patient, EHR, CareProvided, Observation, MedicationAdministered, Prescription,MedicalTreatment



class DPIView(APIView):
    @verify_user
    @verify_role(ROLES.Doctor, ROLES.AdministratifStaff)
    def get(self, request):
        try:
            # get nss
            nss = request.query_params.get('nss', None)
            exact = request.query_params.get('exact', False)
            print('nss=', nss)

            # If NSS is provided
            if nss:
                # search for the patient using NSS
                if exact == "true":
                    patients = Patient.objects.filter(NSS=nss).values()
                    if patients:
                        # get doctor
                        ehr = EHR.objects.filter(id=patients[0]['ehr_id']).values()[0]
                        doctor = Doctor.objects.filter(id=ehr['creator_id']).values()[0]
                        patients[0]['doctor'] = f"{doctor['name']} {doctor['surname']}"
                else:
                    patients = Patient.objects.filter(NSS__startswith=nss).values()

            # If NSS is not provided
            else:
                patients = Patient.objects.all().values()
            
            # return patients
            return JsonResponse({
                'patients': list(patients)
            })
            
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    
    @verify_user
    @verify_role(ROLES.Doctor, ROLES.AdministratifStaff)
    def post(self, request):
        # get from middleware
        user = request.user
        role = request.role
        Model = request.Model
        
        # Get data from request body
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Extract fields from the parsed data
        name = data.get('name')
        surname = data.get('surname')
        address = data.get('address')
        phone_number = data.get('phonenumber')
        contact_person = data.get('contactperson')
        hospital_id = data.get('hospital_id')
        mutual = data.get('mutual')
        nss = data.get('nss')
        bloodType = data.get('bloodType')
        gender = data.get('gender')
        dateOfBirth = data.get('dateOfBirth')

        # For administrative staff, check for referring doctor id
        if role == ROLES.AdministratifStaff.value:
            referring_doctor_id = data.get('referring_doctor_id')
            if not referring_doctor_id:
                return JsonResponse({"error": "Referring doctor ID is required for administratif staff."}, status=400)

        # Validate required fields
        required_fields = [
            'name', 'surname', 'address', 'phonenumber',
            'contactperson', 'hospital_id', 'mutual', 'nss', 'dateOfBirth'
        ]
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f"The field '{field}' is required"}, status=400)

        # Validate NSS uniqueness
        if Patient.objects.filter(NSS=nss).exists():
            return JsonResponse({'error': f'NSS {nss} already exists'}, status=400)

        # Validate phone number format (10 digits)
        phone_pattern = re.compile(r'^[0-9]{10}$')
        if not phone_pattern.match(phone_number):
            return JsonResponse({'error': "Phone number is invalid. It must contain 10 digits."}, status=400)

        # Validate date of birth format (YYYY-MM-DD)
        if not dateOfBirth:
            return JsonResponse({'error': 'Date Of Birth is required.'}, status=400)

        try:
            date_of_birth = datetime.strptime(dateOfBirth, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Retrieve the hospital using hospital_id
        hospital = get_object_or_404(Hospital, id=hospital_id)

        # Start a transaction to ensure both Patient and EHR are created successfully
        with transaction.atomic():
            # Create patient record
            patient = Patient.objects.create(
                NSS=nss,
                name=name,
                surname=surname,
                dateOfBirth=date_of_birth,
                address=address,
                phoneNumber=phone_number,
                mutual=mutual,
                contactPerson=contact_person,
                bloodType=bloodType,
                gender=gender,
                hospital=hospital
            )

            # Create EHR
            if role == ROLES.Doctor.value:
                # Link to doctor
                doctor = user
                ehr = EHR.objects.create(
                    creator=doctor,  # Doctor is the creator of the EHR
                )
                
            elif role == ROLES.AdministratifStaff.value:
                # Find the referring doctor using ID directly
                referring_doctor = get_object_or_404(Doctor, id=referring_doctor_id)
                admin_staff = user.id
                # Create EHR linked to administratif staff and referring doctor
                ehr = EHR.objects.create(
                    creator_staff=admin_staff,  # Administrative staff is the creator of the EHR
                    creator=referring_doctor,   # Referring doctor is set as creator
                )
            
            # Link the EHR to the patient
            patient.ehr = ehr
            patient.save()

            # Return success response with patient and EHR details
            return JsonResponse({
                'message': 'Patient and EHR created successfully',
                'patient': {
                    'id': patient.id,
                    'name': patient.name,
                    'surname': patient.surname,
                    'dateOfBirth': patient.dateOfBirth,
                    'ehr_id': patient.ehr.id,  # Include the EHR ID associated with the patient
                },
                'ehr_id': ehr.id
            })


# def consultation_dpi(request):
#     # Ensure the method is GET
#     if request.method != 'GET':
#         return JsonResponse({'error': 'Invalid request method'}, status=405)

#     # Get JWT from headers
#     token = request.headers.get("Authorization")
#     if not token:
#         return JsonResponse({"error": "Authorization token is missing"}, status=401)

#     token = token.split(" ")[1]  # Assuming Bearer Token

#     try:
#         # Decode JWT
#         decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         role = decoded.get("role", "").strip().lower()  # Normalize role

#         # Validate role
#         valid_roles = ['doctor', 'administratifstaff', 'patient', 'nurse', 'radiologist', 'labtechnician']
#         if role not in valid_roles:
#             return JsonResponse({"error": "Unauthorized role"}, status=403)

#     except jwt.ExpiredSignatureError:
#         return JsonResponse({"error": "Token has expired"}, status=401)
#     except jwt.InvalidTokenError:
#         return JsonResponse({"error": "Invalid token"}, status=401)

#     # Get data from request body (JSON)
#     try:
#         body = json.loads(request.body)
#         ehr_id = body.get('ehr_id')  # Expecting 'ehr_id' in the JSON body
#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON format"}, status=400)

#     if not ehr_id:
#         return JsonResponse({'error': 'ehr_id is required'}, status=400)

#     # Retrieve EHR using ehr_id
#     ehr = get_object_or_404(EHR, id=ehr_id)

#     # Assuming EHR has a ForeignKey to Patient, adjust if needed
#     patient = get_object_or_404(Patient, ehr=ehr)  # Ensure the relationship is correct here

#     # Get biological reports related to the EHR
#     biological_reports = BiologyReport.objects.filter(ehr=ehr).values()

#     # Get radiological reports related to the EHR
#     radiology_reports = RadiologyReport.objects.filter(ehr=ehr)

#     # Convert radiology report imageData to base64 (if it exists)
#     radiology_reports_data = []
#     for report in radiology_reports:
#         if report.imageData:
#             # Convert binary data to base64
#             image_base64 = base64.b64encode(report.imageData).decode('utf-8')
#             radiology_reports_data.append({
#                 'id': report.id,
#                 'type': report.Type,
#                 'imageData': image_base64,  # Include base64 string instead of raw binary
#                 'date': report.date,
#                 'description': report.description,
#             })
#         else:
#             radiology_reports_data.append({
#                 'id': report.id,
#                 'type': report.Type,
#                 'imageData': None,
#                 'date': report.date,
#                 'description': report.description,
#             })

#     # Get prescriptions related to the EHR
#     prescriptions = Prescription.objects.filter(ehr=ehr).values()

#     # Get diagnostics related to the prescriptions
#     diagnostics = Diagnostic.objects.filter(prescription__ehr=ehr).values()

#     # Get consultations related to the diagnostics
#     consultations = Consultation.objects.filter(diagnostic__prescription__ehr=ehr).values()

#     # Get medical certificates related to the EHR
#     medical_certificates = MedicalCertificate.objects.filter(ehr=ehr).values()

#     # Get care provided records related to the EHR
#     care_provided = CareProvided.objects.filter(ehr=ehr)

#     # Extend care_provided with observations and administered medications
#     care_provided_data = []
#     for care in care_provided:
#         # Fetch observations related to the care provided
#         observations = Observation.objects.filter(care_provided=care).values()
        
#         # Fetch administered medications related to the care provided
#         medications = MedicationAdministered.objects.filter(care_provided=care).values()

#         # Append data with observations and medications
#         care_provided_data.append({
#             'id': care.id,
#             'date': care.date,
#             'observations': list(observations),
#             'administered_medications': list(medications)
#         })

#     # Return the aggregated information
#     return JsonResponse({
#         'patient_info': {
#             'name': patient.name,
#             'surname': patient.surname,
#             'date_of_birth': patient.dateOfBirth,
#             'nss': patient.NSS,
#             'blood_type': patient.bloodType,
#             'gender': patient.gender,
#         },
#         'biological_reports': list(biological_reports),
#         'radiological_reports': radiology_reports_data,  # Updated data with base64 images
#         'prescriptions': list(prescriptions),
#         'diagnostics': list(diagnostics),
#         'consultations': list(consultations),
#         'medical_certificates': list(medical_certificates),
#         'care_provided': care_provided_data
#     })


# Custom Authentication Function
def authenticate_request(request):
    # Get JWT from headers
    token = request.headers.get("Authorization")
    if not token:
        return None, JsonResponse({"error": "Authorization token is missing"}, status=401)

    try:
        # Assuming Bearer Token
        token = token.split(" ")[1]

        # Decode JWT
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        role = decoded.get("role", "").strip().lower()  # Normalize role

        # Validate role
        valid_roles = ['doctor', 'administratifstaff', 'patient', 'nurse', 'radiologist', 'labtechnician']
        if role not in valid_roles:
            return None, JsonResponse({"error": "Unauthorized role"}, status=403)

        return decoded, None  # Valid token

    except jwt.ExpiredSignatureError:
        return None, JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return None, JsonResponse({"error": "Invalid token"}, status=401)


# Patient Information View
class PatientInfoView(APIView):
    def get(self, request, nss):
        # Authenticate user
        decoded, error = authenticate_request(request)
        if error:
            return error  # Return auth error if any

        # Fetch patient info
        patient = get_object_or_404(Patient, NSS=nss)
        ehr = get_object_or_404(EHR, id=patient.ehr.id)

        # Retrieve doctor info
        doctor_name = ehr.creator.name if ehr.creator else "Unknown"
        doctor_surname = ehr.creator.surname if ehr.creator else "Unknown"

        return JsonResponse({
            'name': patient.name,
            'surname': patient.surname,
            'date_of_birth': patient.dateOfBirth,
            'nss': patient.NSS,
            'blood_type': patient.bloodType,
            'gender': patient.gender,
            'contact_person': patient.contactPerson,
            'doctor_name': doctor_name,
            'doctor_surname': doctor_surname,
        })

class CareProvidedView(APIView):
    def get(self, request, nss):
        # Authenticate user
        decoded, error = authenticate_request(request)
        if error:
            return error  # Return auth error if any

        # Fetch care provided
        patient = get_object_or_404(Patient, NSS=nss)
        ehr = get_object_or_404(EHR, id=patient.ehr.id)

        care_provided = CareProvided.objects.filter(ehr=ehr)
        care_data = []

        for care in care_provided:
            observations = Observation.objects.filter(care_provided=care)
            medications = MedicationAdministered.objects.filter(care_provided=care)

            # Constructing the care data
            care_data.append({
                'id': care.id,
                'date': care.date,
                'time': care.time.strftime("%H:%M:%S"),
                'care_actions': care.care_actions,
                'nurse': care.nurse.name ,
                'observations': [
                    {
                        'id': observation.id,
                        'description': observation.description
                    }
                    for observation in observations
                ],
                'administered_medications': [
                    {
                        'id': medication.id,
                        'medicine': {
                            'id': medication.medicine.id,
                            'name': medication.medicine.name
                        }
                    }
                    for medication in medications
                ],
            })

        return JsonResponse({'care_provided': care_data})
class PrescriptionView(APIView):
    def get(self, request, prescription_id):
        # Authenticate user
        decoded, error = authenticate_request(request)
        if error:
            return error  # Return auth error if any

        # Fetch the specific prescription by id
        prescription = get_object_or_404(Prescription, id=prescription_id)

        # Fetch related medical treatments for this specific prescription
        medical_treatments = MedicalTreatment.objects.filter(prescription=prescription)

        # Fetch the EHR associated with the prescription
        ehr = prescription.ehr

        # Fetch the patient associated with the same EHR
        patient = get_object_or_404(Patient, ehr=ehr)

        # Prepare prescription data with related medical treatments
        prescription_data = {
            'id': prescription.id,
            'isValid': prescription.isValid,
            'date': prescription.date,
            'doctor': prescription.doctor.id if prescription.doctor else None,
            'ehr': ehr.id if ehr else None,
            'patient': {
                'id': patient.id,
                'nss': patient.NSS,
                'name': patient.name,
                'surname': patient.surname,
                'dateofbirth': patient.dateOfBirth,
                'gender': patient.gender
            },
            'medical_treatments': [
                {
                    'id': treatment.id,
                    'dose': treatment.dose,
                    'duration': treatment.Duration,
                    'medicine': {
                        'id': treatment.medicine.id,
                        'name': treatment.medicine.name
                    }
                }
                for treatment in medical_treatments
            ]
        }

        return JsonResponse({'prescription': prescription_data})



class PatientPrescriptionsView(APIView):
    def get(self, request, nss):
        # Authenticate user
        decoded, error = authenticate_request(request)
        if error:
            return error  # Return auth error if any

        # Fetch the patient by nss
        patient = get_object_or_404(Patient, NSS=nss)

        # Extract the patient's EHR
        ehr = patient.ehr

        # Fetch all prescriptions related to the patient's EHR
        prescriptions = Prescription.objects.filter(ehr=ehr)

        # Prepare the data to return
        data = []

        # Loop through each prescription
        for prescription in prescriptions:
            prescription_data = {
                'prescription_id': prescription.id,
                'prescription_isValid': prescription.isValid,
                'prescription_date': prescription.date,
                'doctor': prescription.doctor.id if prescription.doctor else None,
            }

            # Search for the diagnostic record related to this prescription
            diagnostic = Diagnostic.objects.filter(prescription=prescription).first()

            if diagnostic:
                diagnostic_data = {
                    'diagnostic_id': diagnostic.id,
                }

                # Search for the consultation record related to this diagnostic
                consultation = Consultation.objects.filter(diagnostic=diagnostic).first()

                if consultation:
                    consultation_data = {
                        'consultation_id': consultation.id,
                        'chief_complaint': consultation.chiefComplaint,
                        'date': consultation.date,
                    }

                    # Add consultation data to diagnostic data
                    diagnostic_data['consultation'] = consultation_data

                # Add diagnostic data to prescription data
                prescription_data['diagnostic'] = diagnostic_data

            # Add prescription data to the main data list
            data.append(prescription_data)

        return JsonResponse({'patient_prescriptions_and_consultations': data})
