from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.models import CareProvided, Medecine, MedicationAdministered, Nurse, EHR, Observation
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import jwt
import json

@method_decorator(csrf_exempt, name="dispatch")  # Désactive la vérification CSRF
class CareProvidedCreateView(View):
    def post(self, request):
        # Vérification et validation du token JWT
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            token = token.split(" ")[1]  # Assumer un Bearer Token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded.get("role", "").strip().lower()

            # Vérifier le rôle
            if role != "nurse":
                return JsonResponse({"error": "Unauthorized role"}, status=403)

            # Récupérer le nurse connecté à partir du token
            nurse_id = decoded.get("user_id")  # Assumer que le `user_id` est l'ID du nurse
            nurse = Nurse.objects.get(id=nurse_id)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # Traitement de la création
        try:
            # Parser les données JSON de la requête
            data = json.loads(request.body)
            ehr_id = data.get("ehr_id")
            date = data.get("date")
            time = data.get("time")
            care_actions = data.get("care_actions")
            observation_description = data.get("observation_description")  # Description de l'observation
            medicine_id = data.get("medicine_id")  # ID du médicament

            if not observation_description:
                return JsonResponse({"error": "Observation description is required"}, status=400)

            # Récupérer l'objet EHR et Medecine
            ehr = EHR.objects.get(id=ehr_id)
            medicine = Medecine.objects.get(id=medicine_id)  # Récupérer le médicament

            # Créer l'enregistrement CareProvided
            care_provided = CareProvided.objects.create(
                nurse=nurse,
                ehr=ehr,
                date=date,
                time=time,
                care_actions=care_actions,
            )

            # Créer et attacher une Observation au CareProvided
            observation = Observation.objects.create(
                description=observation_description,
                care_provided=care_provided
            )

            # Créer MedicationAdministered pour ce CareProvided
            medication_administered = MedicationAdministered.objects.create(
                care_provided=care_provided,
                medicine=medicine  # Relier le médicament
            )

            # Inclure le nom du nurse dans la réponse
            return JsonResponse(
                {
                    "id": care_provided.id,
                    "observation_id": observation.id,
                    "medication_administered_id": medication_administered.id,
                    "nurse_name": nurse.name,  # Nom du nurse connecté
                    "message": "Care provided, observation, and medication administered created successfully",
                },
                status=201,
            )

        except Nurse.DoesNotExist:
            return JsonResponse({"error": "Nurse not found"}, status=404)
        except EHR.DoesNotExist:
            return JsonResponse({"error": "EHR not found"}, status=404)
        except Medecine.DoesNotExist:
            return JsonResponse({"error": "Medicine not found"}, status=404)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

# Pour la mise à jour et les détails, voici les modifications à apporter dans les autres vues.

@method_decorator(csrf_exempt, name="dispatch")  # Désactive la vérification CSRF
class CareProvidedUpdateView(View):
    def post(self, request, care_provided_id):
        # Vérification du token JWT
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            token = token.split(" ")[1]  # Assumer un Bearer Token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            nurse_id = decoded.get("user_id")  # ID du nurse dans le token
            nurse = Nurse.objects.get(id=nurse_id)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # Traitement de la mise à jour
        try:
            data = json.loads(request.body)
            date = data.get("date")
            time = data.get("time")
            care_actions = data.get("care_actions")
            observation_description = data.get("observation_description")
            medicine_id = data.get("medicine_id")  # ID du médicament

            # Récupérer l'enregistrement CareProvided
            care_provided = CareProvided.objects.get(id=care_provided_id)

            # Mettre à jour les champs de CareProvided
            if date:
                care_provided.date = date
            if time:
                care_provided.time = time
            if care_actions:
                care_provided.care_actions = care_actions

            care_provided.save()

            # Mettre à jour ou créer une Observation associée
            if observation_description:
                observation, created = Observation.objects.get_or_create(
                    care_provided=care_provided
                )
                observation.description = observation_description
                observation.save()

            # Mettre à jour ou créer MedicationAdministered
            if medicine_id:
                medicine = Medecine.objects.get(id=medicine_id)
                medication_administered, created = MedicationAdministered.objects.get_or_create(
                    care_provided=care_provided
                )
                medication_administered.medicine = medicine
                medication_administered.save()

            return JsonResponse(
                {
                    "message": "CareProvided, observation, and medication administered updated successfully",
                    "care_provided_id": care_provided.id,
                    "medication_administered_id": medication_administered.id if medicine_id else None,
                    "nurse_name": nurse.name  # Nom du nurse connecté
                },
                status=200,
            )

        except CareProvided.DoesNotExist:
            return JsonResponse({"error": "CareProvided not found"}, status=404)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

# Vue de détail
@method_decorator(csrf_exempt, name="dispatch")  # Désactive la vérification CSRF
class CareProvidedDetailView(View):
    def get(self, request, care_provided_id):
        # Vérification du token JWT
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            token = token.split(" ")[1]
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            nurse_id = decoded.get("user_id")  # ID du nurse dans le token
            nurse = Nurse.objects.get(id=nurse_id)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # Si l'utilisateur est authentifié, récupérer les détails
        try:
            care_provided = CareProvided.objects.get(id=care_provided_id)

            observations = care_provided.observations.all()
            medications_administered = care_provided.medications_administered.all()

            observation_data = [
                {
                    'id': observation.id,
                    'description': observation.description
                } for observation in observations
            ]

            medication_data = [
                {
                    'medicine_name': medication.medicine.name,
                } for medication in medications_administered
            ]

            return JsonResponse({
                'id': care_provided.id,
                'nurse_id': care_provided.nurse.id,
                'nurse_name': nurse.name,  # Nom du nurse connecté
                'ehr_id': care_provided.ehr.id,
                'date': care_provided.date,
                'time': care_provided.time,
                'care_actions': care_provided.care_actions,
                'observations': observation_data,
                'medications_administered': medication_data
            }, status=200)

        except CareProvided.DoesNotExist:
            return JsonResponse({'error': 'CareProvided not found'}, status=404)
