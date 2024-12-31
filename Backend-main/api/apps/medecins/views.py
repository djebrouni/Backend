
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


@method_decorator(csrf_exempt, name='dispatch')  # Désactive la vérification CSRF
class ConsultationSummaryView(View):
    def get(self, request, consultation_id):
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

def get_user_role_from_token(request):
    """
    Extract user role from the Authorization token.
    """
    token = request.headers.get("Authorization")
    if not token:
        return None, JsonResponse({"error": "Authorization token is missing"}, status=401)
    try:
        # Extract and decode the token
        token = token.split(" ")[1]  # Assuming Bearer Token
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
