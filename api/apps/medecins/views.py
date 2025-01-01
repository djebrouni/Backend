from django.http import JsonResponse
import jwt
from django.conf import settings
from api.models import Patient, EHR
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.models import Consultation, Diagnostic
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.models import Consultation, Diagnostic
from django.conf import settings
import jwt
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

@method_decorator(csrf_exempt, name='dispatch')  # Désactive la vérification CSRF
class ConsultationSummaryView(View):
    def get(self, request, consultation_id):
        # Vérification du token JWT
        error_response = validate_user_token(request)
        if error_response:  # Si le token est invalide ou manquant
            return error_response

        try:
            # Récupérer l'objet Consultation existant
            consultation = Consultation.objects.get(id=consultation_id)

            # Inclure le diagnostic dans la réponse
            diagnostic_id = consultation.diagnostic.id if consultation.diagnostic else None

            # Retourner le résumé (summary) de la consultation et l'ID du diagnostic
            return JsonResponse({
                'summary': consultation.summary,
                'diagnostic_id': diagnostic_id
            }, status=200)

        except Consultation.DoesNotExist:
            return JsonResponse({'error': 'Consultation not found'}, status=404)


def validate_user_token(request):
    """
    Validate the Authorization token.
    """
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Authorization token is missing"}, status=401)
    try:
        # Extract and decode the token
        token = token.split(" ")[1]  # Assuming Bearer Token
        jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return None  # Token is valid
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

@method_decorator(csrf_exempt, name='dispatch')
class ConsultationCreateView(View):
    def post(self, request):
        # Check user role
        role, error_response = get_user_role_from_token(request)
        if error_response:
            return error_response
        if role != "doctor":
            return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)

        try:
            # Parse the JSON request
            data = json.loads(request.body)

            # Extract fields
            date = data.get('date')
            summary = data.get('summary')
            chief_complaint = data.get('chief_complaint')

            # Create a new diagnostic
            diagnostic = Diagnostic.objects.create()

            # Create consultation and associate diagnostic
            consultation = Consultation.objects.create(
                date=date,
                summary=summary,
                chiefComplaint=chief_complaint,
                diagnostic=diagnostic
            )

            return JsonResponse({
                'consultation_id': consultation.id,
                'diagnostic_id': diagnostic.id,
                'message': 'Consultation and Diagnostic created successfully'
            }, status=201)

        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ConsultationUpdateView(View):
    def post(self, request, consultation_id):
        # Check user role
        role, error_response = get_user_role_from_token(request)
        if error_response:
            return error_response
        if role != "doctor":
            return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)

        try:
            # Parse the JSON request
            data = json.loads(request.body)

            # Extract fields
            summary = data.get('summary')
            chief_complaint = data.get('chief_complaint')

            # Retrieve and update consultation
            consultation = Consultation.objects.get(id=consultation_id)
            consultation.summary = summary if summary else consultation.summary
            consultation.chiefComplaint = chief_complaint if chief_complaint else consultation.chiefComplaint
            consultation.save()

            return JsonResponse({'message': 'Consultation updated successfully'}, status=200)

        except Consultation.DoesNotExist:
            return JsonResponse({'error': 'Consultation not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
