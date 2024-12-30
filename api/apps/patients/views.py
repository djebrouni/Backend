from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from api.models import Patient, EHR, Doctor, administratifStaff, Hospital
import json
import jwt
from django.conf import settings
from datetime import datetime
import re
from api.helper.getModels import getModel


@csrf_exempt
def create_patient_dpi(request):
    # Ensure the method is POST
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Get JWT from headers
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Authorization token is missing"}, status=401)
    token = token.split(" ")[1]  # Assuming Bearer Token
    try:
        # Decode JWT
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        role = decoded.get("role", "").strip().lower()  # Normalize role

        # Pass role to getModel
        model = getModel(role)  # Validate role here
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

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

    # For administrative staff, check for referring doctor name and surname
    if role == 'administratifstaff':
        referring_doctor_name = data.get('referring_doctor_name')
        referring_doctor_surname = data.get('referring_doctor_surname')
        if not referring_doctor_name or not referring_doctor_surname:
            return JsonResponse({"error": "Referring doctor name and surname are required for administratif staff."}, status=400)

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
        if role == 'doctor':
            doctor = get_object_or_404(Doctor, id=decoded.get('user_id'))  # Use the decoded user_id or any identifier in your JWT
            # Create EHR linked to doctor
            ehr = EHR.objects.create(
                creator=doctor,  # Doctor is the creator of the EHR
            )
        elif role == 'administratifstaff':
            # Find the referring doctor
            referring_doctor = Doctor.objects.filter(name=referring_doctor_name, surname=referring_doctor_surname).first()

            if not referring_doctor:
                return JsonResponse({"error": "Referring doctor does not exist."}, status=400)

            admin_staff = get_object_or_404(administratifStaff, id=decoded.get('user_id'))
            # Create EHR linked to administratif staff and referring doctor
            ehr = EHR.objects.create(
                creator_staff=admin_staff,  # Administrative staff is the creator of the EHR
                creator=referring_doctor,   # Referring doctor is set as creator
            )
        else:
            # If the role is neither doctor nor administratifStaff, rollback the transaction and return error
            return JsonResponse({"error": "Invalid role for EHR creation"}, status=400)

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
