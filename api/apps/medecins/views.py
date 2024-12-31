from django.http import JsonResponse
import jwt
from django.conf import settings
from api.models import Patient, EHR
import json

def rechercheDpiParNss(request):
    # Ensure the method is GET
    if request.method != 'GET':
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

        # Validate role
        valid_roles = ['doctor', 'administratifstaff']
        if role not in valid_roles:
            return JsonResponse({"error": "Unauthorized role"}, status=403)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

    

    try:

        # Parse JSON input
        data = json.loads(request.body.decode('utf-8'))
        nss = data.get('nss')

        if not nss:
            return JsonResponse({"error": "Missing 'nss' parameter"}, status=400)
        # Search for the patient using NSS
        patient = Patient.objects.get(NSS=nss)
        ehr = EHR.objects.get(patient=patient)

        # Return the EHR ID and patient details
        return JsonResponse({
            'ehr_id': ehr.id,
            'name': patient.name,
            'surname': patient.surname,
            'nss': patient.NSS
        })
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)
    except EHR.DoesNotExist:
        return JsonResponse({'error': 'EHR not found for this patient'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
