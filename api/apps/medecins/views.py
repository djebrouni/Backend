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
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from api.models import EHR, BiologicalAssessment
import json
import jwt
from django.conf import settings


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
def get_user_role_from_token(request):
    """
    Extrait le rôle de l'utilisateur à partir du token d'autorisation.
    """
    token = request.headers.get("Authorization")
    if not token:
        return None, JsonResponse({"error": "Authorization token is missing"}, status=401)
    try:
        # Extraire et décoder le token
        token = token.split(" ")[1]  # En supposant que le token est un Bearer Token
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded.get("role", "").strip().lower(), None
    except jwt.ExpiredSignatureError:
        return None, JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return None, JsonResponse({"error": "Invalid token"}, status=401)


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
        



#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::CREATION DU BILAN ASSESMET ET SON DISPLAY:::::::::::::::::::::::::::::::::::::::

@method_decorator(csrf_exempt, name='dispatch')
class DisplayBiologicalAssessmentView(View):
    def authenticate_user(self, request):
        """
        Vérifie si l'utilisateur est authentifié à l'aide du token d'autorisation.
        """
        token = request.headers.get("Authorization")
        if not token:
            return False, JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            token = token.split(" ")[1]  # En supposant que le token est un Bearer Token
            jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return True, None
        except jwt.ExpiredSignatureError:
            return False, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return False, JsonResponse({"error": "Invalid token"}, status=401)

    def get(self, request, ehr_id):
        # Vérification de l'authentification
        is_authenticated, error_response = self.authenticate_user(request)
        if not is_authenticated:
            return error_response

        # Vérification si le bilan biologique existe pour l'EHR donné
        biological_assessment = get_object_or_404(BiologicalAssessment, ehr_id=ehr_id)

        # Structurer les données pour la réponse JSON
        response_data = {
            "date": biological_assessment.date.strftime("%Y-%m-%d"),
            "patient_name": biological_assessment.patient_name,
            "date_of_birth": biological_assessment.date_of_birth.strftime("%Y-%m-%d"),
            "age": biological_assessment.age,
            "gender": biological_assessment.gender,
            "tests_to_conduct": biological_assessment.tests_to_conduct,
        }

        return JsonResponse(response_data, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class CreateBiologicalAssessmentView(View):
    def get_user_role_from_token(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            token = token.split(" ")[1]  # En supposant que le token est un Bearer Token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return decoded.get("role", "").strip().lower(), None
        except jwt.ExpiredSignatureError:
            return None, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return None, JsonResponse({"error": "Invalid token"}, status=401)

    def post(self, request, ehr_id):
        # Vérification du rôle de l'utilisateur
        role, error_response = self.get_user_role_from_token(request)
        if error_response:
            return error_response
        if role != "doctor":
            return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)

       
        # Récupérer l'EHR du patient
        ehr = get_object_or_404(EHR, id=ehr_id)

        # Récupérer les données JSON envoyées par le médecin
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        # Extraction des données de la requête
        date = data.get('date')
        patient_name = data.get('patient_name')
        date_of_birth = data.get('date_of_birth')
        age = data.get('age')
        gender = data.get('gender')
        tests_to_conduct = data.get('tests_to_conduct')

        # Validation des champs requis
        if not date or not patient_name or not date_of_birth or not age or not gender or not tests_to_conduct:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # Conversion de la date au format YYYY-MM-DD
        try:
            formatted_date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            return JsonResponse({"error": "Invalid date format. It must be in DD/MM/YYYY format."}, status=400)

        # Création de l'évaluation biologique
        biological_assessment = BiologicalAssessment.objects.create(
            date=formatted_date,
            patient_name=patient_name,
            date_of_birth=date_of_birth,
            age=age,
            gender=gender,
            tests_to_conduct=tests_to_conduct,
            ehr=ehr,
           
        )

        return JsonResponse({'message': 'Biological assessment created successfully', 'assessment_id': biological_assessment.id})

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::REMPLIR LE BILAN ET SON DISPLAY::::::::::::::::::::::::::::::::::::::::::::::::::::::::
