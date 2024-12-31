from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.models import CareProvided, Nurse, EHR
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.models import CareProvided, Nurse, EHR
from django.conf import settings
import jwt
import json

def getModel(role):
    """
    Fonction fictive pour valider le rôle et retourner un modèle ou une exception.
    """
    if role == "nurse":
        return Nurse
    raise ValueError("Invalid role")


@method_decorator(csrf_exempt, name="dispatch")  # Désactive la vérification CSRF
class CareProvidedCreateView(View):
    def post(self, request):
        # Récupérer et valider le token JWT
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            # Assumer un Bearer Token
            token = token.split(" ")[1]
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded.get("role", "").strip().lower()

            # Vérifier le rôle
            if role != "nurse":
                return JsonResponse({"error": "Unauthorized role"}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        # Traitement de la création
        try:
            # Parser les données JSON de la requête
            data = json.loads(request.body)
            nurse_id = data.get("nurse_id")
            ehr_id = data.get("ehr_id")
            date = data.get("date")
            time = data.get("time")
            care_actions = data.get("care_actions")

            # Récupérer les objets associés
            nurse = Nurse.objects.get(id=nurse_id)
            ehr = EHR.objects.get(id=ehr_id)

            # Créer un enregistrement
            care_provided = CareProvided.objects.create(
                nurse=nurse,
                ehr=ehr,
                date=date,
                time=time,
                care_actions=care_actions,
            )

            return JsonResponse(
                {"id": care_provided.id, "message": "Care provided created successfully"},
                status=201,
            )

        except Nurse.DoesNotExist:
            return JsonResponse({"error": "Nurse not found"}, status=404)
        except EHR.DoesNotExist:
            return JsonResponse({"error": "EHR not found"}, status=404)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")  # Désactive la vérification CSRF
class CareProvidedUpdateView(View):
    def post(self, request, care_provided_id):
        # Récupérer et valider le token JWT
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            # Assumer un Bearer Token
            token = token.split(" ")[1]
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded.get("role", "").strip().lower()

            # Vérifier le rôle
            if role != "nurse":
                return JsonResponse({"error": "Unauthorized role"}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        # Traitement de la mise à jour
        try:
            data = json.loads(request.body)
            date = data.get("date")
            time = data.get("time")
            care_actions = data.get("care_actions")

            # Récupérer l'enregistrement
            care_provided = CareProvided.objects.get(id=care_provided_id)

            # Mettre à jour les champs
            if date:
                care_provided.date = date
            if time:
                care_provided.time = time
            if care_actions:
                care_provided.care_actions = care_actions

            care_provided.save()
            return JsonResponse(
                {"message": "CareProvided updated successfully"}, status=200
            )

        except CareProvided.DoesNotExist:
            return JsonResponse({"error": "CareProvided not found"}, status=404)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
@method_decorator(csrf_exempt, name='dispatch')  # Désactive la vérification CSRF
class CareProvidedDetailView(View):
    def get(self, request, care_provided_id):
        try:
            # Récupérer l'objet CareProvided existant
            care_provided = CareProvided.objects.get(id=care_provided_id)

            # Retourner les informations de l'objet CareProvided
            return JsonResponse({
                'id': care_provided.id,
                'nurse_id': care_provided.nurse.id,
                'ehr_id': care_provided.ehr.id,
                'date': care_provided.date,
                'time': care_provided.time,
                'care_actions': care_provided.care_actions
            }, status=200)

        except CareProvided.DoesNotExist:
            return JsonResponse({'error': 'CareProvided not found'}, status=404)
 